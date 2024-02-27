from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import base64
import io
import numpy as np
import json
import random
import pandas as pd
from scipy.stats import linregress
from scipy.optimize import curve_fit

np.seterr(divide='raise')
# 将除0设置为error级

def decode_base64_image(base64_encoded_image):
    # 用于将base64编码转换为图片格式，包含对传入图片编码的识别
    header, encoded = base64_encoded_image.split(',', 1)
    image_format , _ = header.split(';')
    image_format = image_format.split('/')[1]
    decoded_image = base64.b64decode(encoded)
    nparr = np.frombuffer(decoded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def create_function(expression):
    # 将用户输入的计算式转换为函数
    def function(B, G, R): return eval(expression)
    return function

def linear(x,m,b):
    # 定义直线模型
    return m*x + b

app = FastAPI()

methord = 1 # 用于设置切换拟合算法，
            # 当该值为1时使用lineregress即不考虑数据点误差方法；
            # 为2时使用curve_fit方法，数据点误差为权重的倒数

async def process_image(websocket: WebSocket):
    while True:
        try:
            data = await websocket.receive_text()
            if not data:
                break
            print("Data Recieved")
            messageIn = json.loads(data)
            # print(data)
            orImg = decode_base64_image(messageIn['image'])
            circles = pd.read_csv(io.StringIO(messageIn['circles'])).values
            userFunc = create_function(messageIn['function'])
            xValueIn = pd.read_csv(io.StringIO(messageIn['xValue'])).values
            # print("Data Processed")
            results = []
            for circle in circles:
                points = [(random.randint(circle[0]-circle[2], circle[0]+circle[2]), 
                            random.randint(circle[1]-circle[2], circle[1]+circle[2])) 
                            for _ in range(20)]
                # 在每个圆范围内随机取点20个
                rat = []
                for x, y in points:
                    try:
                        rat.append(userFunc(orImg[y, x, 0], orImg[y, x, 1], orImg[y, x, 2]))
                        # 根据用户定义函数计算每个随机点的数值
                    except Exception as e:
                        await websocket.send_text(json.dumps({'status': 'error', 'error': str(e)}))
                results.append(rat)
            
            sumResult = []
            yValues = []
            xValues = []
            for res in results:
                # 计算平均值和标准差
                sumResult.append([np.mean(res), np.std(res)])
                yValues.append(np.mean(res))
            for x in xValueIn:
                # xValueIn中格式为[[x0],[x1],[x2]]，需要先转换为一维数组
                xValues.append(x[0])
            if methord == 1:
                slope, intercept, r_value, p_value, std_err = linregress(xValues, yValues)
                await websocket.send_text(json.dumps({'status': 'success', 'result': [slope, intercept, r_value*r_value, p_value, std_err]}))
                print(slope, intercept, r_value, p_value, std_err)
            elif methord == 2:
                weight = [1/row[1] for row in sumResult]
                params,covariance = curve_fit(linear,xValues,yValues,sigma=weight)
                mfit , bfit = params
                y_fit=linear(np.array(xValues),mfit,bfit)
                TSS = np.sum((yValues - np.mean(yValues))**2)
                RSS = np.sum((yValues - y_fit)**2)
                R_squared = 1 - (RSS / TSS)
            await websocket.send_text(json.dumps({'status': 'success', 'result': [mfit, bfit, R_squared]}))
        except WebSocketDisconnect:
            print("Client Disconnected")
            break
        finally:
            await websocket.close()
            break

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await process_image(websocket)