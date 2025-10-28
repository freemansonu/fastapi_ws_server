from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Client connected!")
    while True:
        print(".")
        data = await websocket.receive_text()   # Receive message from Flutter
        print("📩 Received:", data)
        await websocket.send_text(f"Server says: Hi, you said '{data}'!")  # Send reply