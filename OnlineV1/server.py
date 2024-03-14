import json
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from fastapi import FastAPI, WebSocket
import cv2
import base64
import io
import numpy as np
import random
import pandas as pd
from scipy.stats import linregress
from scipy.optimize import curve_fit
import asyncio


np.seterr(divide='ignore')
# 将除0设置为error级


def decode_base64_image(base64_encoded_image):
    # 用于将base64编码转换为图片格式，包含对传入图片编码的识别
    header, encoded = base64_encoded_image.split(',', 1)
    image_format, _ = header.split(';')
    image_format = image_format.split('/')[1]
    decoded_image = base64.b64decode(encoded)
    nparr = np.frombuffer(decoded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def create_function(expression):
    # 将用户输入的计算式转换为函数
    def function(B, G, R): return eval(expression)
    return function


def linear(x, m, b):
    # 定义直线模型
    return m*x + b


def is_nan(value):
    return value != value


async def send_status(websocket, iteration, r_squared):
    sendStatus = json.dumps(
        {"status": "busy", "iteration": iteration + 1, "R2": r_squared})
    await websocket.send_text(sendStatus)
    # print(sendStatus)


async def train_model(websocket, messageIn, trainData):
    # 进行自动计算
    goalR2 = float(messageIn['Goal'])
    # 解算目标R2
    iterations = int(messageIn['iteration'])
    # 目标迭代次数
    trainDataDf = pd.DataFrame(
        trainData, columns=['R', 'G', 'B', 'x'])
    RGB_values = trainDataDf[['R', 'G', 'B']].values
    concentration_values = trainDataDf['x'].values

    # 初始化参数和优化器
    parameters = np.random.rand(6)
    optimizer = {'beta1': 0.9, 'beta2': 0.999, 'epsilon': 1e-8}
    m = np.zeros(6)
    v = np.zeros(6)

    # 模型训练
    for iteration in range(iterations):
        model_output = np.dot(
            RGB_values, parameters[:3]) / np.dot(RGB_values, parameters[3:])
        combined_data = np.column_stack(
            (concentration_values, model_output))
        linear_reg_model = LinearRegression()
        linear_reg_model.fit(
            combined_data[:, 0].reshape(-1, 1), combined_data[:, 1])
        r_squared = r2_score(combined_data[:, 1], linear_reg_model.predict(
            combined_data[:, 0].reshape(-1, 1)))
        gradient = np.zeros(6)
        for i in range(3):
            gradient[i] = np.sum(2 * (model_output - concentration_values)
                                 * RGB_values[:, i] / np.dot(RGB_values, parameters[3:]))
        for i in range(3, 6):
            gradient[i] = np.sum(-2 * (model_output - concentration_values) *
                                 model_output * RGB_values[:, i-3] / np.dot(RGB_values, parameters[3:])**2)
        m = optimizer['beta1'] * m + \
            (1 - optimizer['beta1']) * gradient
        v = optimizer['beta2'] * v + \
            (1 - optimizer['beta2']) * (gradient ** 2)
        m_hat = m / (1 - optimizer['beta1'] ** (iteration + 1))
        v_hat = v / (1 - optimizer['beta2'] ** (iteration + 1))
        parameters -= m_hat / \
            (np.sqrt(v_hat) + optimizer['epsilon'])
        if (iteration % 100) == 9:
            asyncio.create_task(send_status(websocket, iteration, r_squared))
            # print(iteration, r_squared)
        if r_squared > goalR2:
            break
        await asyncio.sleep(0)
    return r_squared, parameters

app = FastAPI()

methord = 1  # 用于设置切换拟合算法，
# 当该值为1时使用lineregress即不考虑数据点误差方法；
# 为2时使用curve_fit方法，数据点误差为权重的倒数

notAutoFunc = True  # 切换是否使用自动求解器

userFunc = None
# 用于计算的函数

randomNum = 20
# 所选范围内随机取点个数

linearResult = None


async def process_image_standerd(websocket: WebSocket):
    try:
        data = await websocket.receive_text()
        # 从前端接收数据
        if not data:
            pass
        print("Data Recieved")

        messageIn = json.loads(data)
        if messageIn['methord'] == True:
            methord = 2
        else:
            methord = 1
        # 线性拟合方法，非必须参数，缺省时为1
        notAutoFunc = not messageIn['notAutoFunc']
        # 是否自动求解方程，非必须参数，缺省为True即不自动求解
        if str(notAutoFunc) == "":
            notAutoFunc = True
        orImg = decode_base64_image(messageIn['image'])
        # 传入原始图像，必须参数
        circles = pd.read_csv(io.StringIO(
            messageIn['circles']), header=None).values
        # 传入圆坐标、半径[x,y,r]，必须参数
        xValueIn = pd.read_csv(io.StringIO(
            messageIn['xValue']), header=None).values
        # 传入横坐标即为浓度数值，必须参数

        trainData = []
        # 存储用于训练的数据
        results = []

        if notAutoFunc == True:
            userFunc = create_function(messageIn['function'])
        points = []
        for index, circle in enumerate(circles):
            points.append([(random.randint(circle[0]-circle[2], circle[0]+circle[2]),
                            random.randint(circle[1]-circle[2], circle[1]+circle[2]))
                           for _ in range(randomNum)])
            # 用于随机获取采样点，每个圆范围内20个
            if notAutoFunc == True:
                # 不使用自动求解器
                rat = []
                for x, y in points[index]:
                    rat.append(
                        userFunc(orImg[y, x, 0], orImg[y, x, 1], orImg[y, x, 2]))
                    # 使用用户设置的方程计算
                results.append(rat)
            elif notAutoFunc == False:
                # 使用自动求解器
                for point in points[index]:
                    x = point[0]
                    y = point[1]
                    # 遍历点坐标处的数据以加载到用于训练的数据
                    trainDataNow = [
                        orImg[y, x, 2], orImg[y, x, 1], orImg[y, x, 0], xValueIn[index][0]]
                    trainData.append(trainDataNow)
        if notAutoFunc == False:
            r_squared, parameters = await train_model(websocket, messageIn, trainData)
            final_output = {"status": "done", "R2": r_squared,
                            "Model": f"({parameters[0]}*R + {parameters[1]}*G + {parameters[2]}*B) / ({parameters[3]}*R + {parameters[4]}*G + {parameters[5]}*B)"}
            userFunc = create_function(final_output["Model"])
            # 使用计算出的结果创建自定义函数
            await websocket.send_text(json.dumps(final_output))

            for index, circle in enumerate(circles):
                rat = []
                for x, y in points[index]:
                    rat.append(
                        userFunc(orImg[y, x, 0], orImg[y, x, 1], orImg[y, x, 2]))
                results.append(rat)
        sumResult = []
        yValues = []
        xValues = []
        drawPoints = []
        for index, res in enumerate(results):
            # 计算平均值和标准差
            sumResult.append([np.mean(res), np.std(res)])
            yValues.append(np.mean(res))
            drawPoints.append([float(xValueIn[index][0]), float(
                np.mean(res)), float(np.std(res))])
        for x in xValueIn:
            # xValueIn中格式为[[x0],[x1],[x2]]，需要先转换为一维数组
            xValues.append(x[0])
        if methord == 1:
            slope, intercept, r_value, p_value, std_err = linregress(
                xValues, yValues)
            if (is_nan(slope) or is_nan(intercept) or is_nan(r_value)):
                slope = 0
                intercept = 0
                r_value = 0
                drawPoints = []
                # 当输入参数错误导致直线拟合结果异常时将其重置为0
            dataSend = {
                'status': 'success',
                'result': [slope, intercept, float(r_value) * float(r_value)],
                'points': drawPoints
            }
            dataSendJson = json.dumps(dataSend)
            await websocket.send_text(dataSendJson)
            await websocket.close()
        elif methord == 2:
            weight = [1/row[1] for row in sumResult]
            params, covariance = curve_fit(
                linear, xValues, yValues, sigma=weight)
            slope, intercept = params
            y_fit = linear(np.array(xValues), slope, intercept)
            TSS = np.sum((yValues - np.mean(yValues))**2)
            RSS = np.sum((yValues - y_fit)**2)
            R_squared = 1 - (RSS / TSS)
            dataSend = {
                'status': 'success',
                'result': [slope, intercept, R_squared],
                'points': drawPoints
            }
            dataSendJson = json.dumps(dataSend)
            await websocket.send_text(dataSendJson)
            await websocket.close()
    except Exception as e:
        await websocket.close()


async def process_image_sample(websocket: WebSocket):
    try:
        data = await websocket.receive_text()
        if not data:
            pass
        messageIn = json.loads(data)
        smpImg = decode_base64_image(messageIn['image'])
        # 传入样品图片，必须参数
        userFunc = create_function(messageIn['func'])
        # 传入处理函数，由于fastapi服务端无法储存客户端两次的信息，该参数为必须参数
        slope = float(messageIn['slope'])
        # 传入标曲斜率，同上，必须参数
        intercept = float(messageIn['intercept'])
        # 传入标曲截距，同上，必须参数
        # 读取样品图片
        circles = pd.read_csv(io.StringIO(
            messageIn['circle']), header=None).values
        # 读取样品采样区域
        points = []
        results = []
        for index, circle in enumerate(circles):
            points.append([(random.randint(circle[0]-int(circle[2]/1.42), circle[0]+int(circle[2]/1.42)),
                            random.randint(circle[1]-int(circle[2]/1.42), circle[1]+int(circle[2]/1.42)))
                           for _ in range(randomNum)])
            rat = []
            for x, y in points[index]:
                rat.append(userFunc(smpImg[y, x, 0],
                                    smpImg[y, x, 1], smpImg[y, x, 2]))
                # 在选定范围内随机取点并根据函数计算
            results.append(rat)
        result = [np.mean(results), np.std(results)]
        smpRes = [(result[0]-intercept)/slope, result[1]/slope]
        if is_nan(result[0]) or is_nan(result[1]):
            smpRes = [0, 0]
        await websocket.send_text(json.dumps({"status": "done", "result": smpRes}))
        # 传回处理结果，格式为{"status": "done", "result": [result,result_err]}
        await websocket.close()
    except Exception as e:
        await websocket.close()


@app.websocket("/standard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await process_image_standerd(websocket)


@app.websocket("/sample")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await process_image_sample(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
