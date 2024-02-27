import json
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.websocket("/train")
async def train_model(websocket: WebSocket):
    await websocket.accept()

    # 接收并解析客户端发送的消息
    async for message in websocket.iter_text():
        message_data = json.loads(message)
        num_iterations = int(message_data["num_iterations"])
        goalR2 = float(message_data["goal"])
        csv1_content = message_data["csv1"]
        csv2_content = message_data["csv2"]


        # 解析 CSV 内容
        rgb_data = pd.read_csv(StringIO(csv1_content))
        concentration_data = pd.read_csv(StringIO(csv2_content))

        # 将数据转换为 NumPy 数组
        RGB_values = rgb_data[['R', 'G', 'B']].values
        concentration_values = concentration_data['Concentration'].values

        # 初始化参数
        parameters = np.random.rand(6)
        beta1 = 0.9
        beta2 = 0.999
        epsilon = 1e-8
        m = np.zeros(6)
        v = np.zeros(6)

        # 训练过程
        for iteration in range(num_iterations):
            model_output = np.dot(RGB_values, parameters[:3]) / np.dot(RGB_values, parameters[3:])
            combined_data = np.column_stack((concentration_values, model_output))
            linear_reg_model = LinearRegression()
            linear_reg_model.fit(combined_data[:, 0].reshape(-1, 1), combined_data[:, 1])
            r_squared = r2_score(combined_data[:, 1], linear_reg_model.predict(combined_data[:, 0].reshape(-1, 1)))
            gradient = np.zeros(6)
            for i in range(3):
                gradient[i] = np.sum(2 * (model_output - concentration_values) * RGB_values[:, i] / np.dot(RGB_values, parameters[3:]))
            for i in range(3, 6):
                gradient[i] = np.sum(-2 * (model_output - concentration_values) * model_output * RGB_values[:, i-3] / np.dot(RGB_values, parameters[3:])**2)
            m = beta1 * m + (1 - beta1) * gradient
            v = beta2 * v + (1 - beta2) * (gradient ** 2)
            m_hat = m / (1 - beta1 ** (iteration + 1))
            v_hat = v / (1 - beta2 ** (iteration + 1))
            parameters -= m_hat / (np.sqrt(v_hat) + epsilon)
            if(iteration % 100 ) == 9:
                # 实时发送进度信息
                message = {"status":"busy","iteration": iteration + 1, "R2": r_squared}
                await websocket.send_text(json.dumps(message))
            if(r_squared > goalR2):
                break

        # 返回最终结果
        final_output = {"status":"done","R2": r_squared,"Model": f"({parameters[0]}*R + {parameters[1]}*G + {parameters[2]}*B) / ({parameters[3]}*R + {parameters[4]}*G + {parameters[5]}*B)"}
        await websocket.send_text(json.dumps(final_output))
        await websocket.close()
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
