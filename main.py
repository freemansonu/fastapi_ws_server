from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Client connected!")

    async def send_waiting():
        while True:
            await asyncio.sleep(3)  # Wait 3 minute
            try:
                await websocket.send_text("#")
            except Exception as e:
                print("⚠️ Error sending waiting:", e)
                break

    # Start background task
    asyncio.create_task(send_waiting())

    # Main loop: receive messages from client
    try:
        while True:
            data = await websocket.receive_text()
            print("📩 Received:", data)
            await websocket.send_text(f"Server says: Hi, you said '{data}'!")
    except Exception as e:
        print("❌ Client disconnected:", e)
