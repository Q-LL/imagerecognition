import json
from fastapi import FastAPI, WebSocket
import time

app = FastAPI()

async def process_image_standerd(websocket: WebSocket):
    data = await websocket.receive_text()
    print("Data Recieved")
    messageIn = json.loads(data)
    for i in range(int(messageIn['iteration'])):
        time.sleep(0.1)
        sendStatus = json.dumps(
                        {"status": "busy", "iteration": i + 1, "R2": 0})
        await websocket.send_text(sendStatus)
        print(sendStatus)

@app.websocket("/standard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await process_image_standerd(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
