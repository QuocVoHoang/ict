from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from datetime import datetime

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    
    try:
        while True:
            # Send message every 5 seconds
            message = {
                "timestamp": datetime.now().isoformat(),
                "message": "Hello from backend!",
                "data": "This is a periodic message"
            }
            await websocket.send_text(json.dumps(message))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")