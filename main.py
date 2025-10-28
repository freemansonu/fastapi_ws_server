from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI WebSocket server running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Client connected!")

    async def send_waiting():
        while True:
            await asyncio.sleep(60)  # send every minute
            try:
                await websocket.send_text("waiting")
            except Exception as e:
                print("⚠️ Error sending waiting:", e)
                break

    asyncio.create_task(send_waiting())

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Server says: You said '{data}'")
    except Exception as e:
        print("❌ Client disconnected:", e)
