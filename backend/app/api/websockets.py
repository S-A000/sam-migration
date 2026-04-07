from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

# Connection Manager: Taake humein pata ho kaun kaun se users online hain
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_log(self, message: str):
        """Pure UI Terminal par log bhejne ke liye"""
        for connection in self.active_connections:
            await connection.send_json({"type": "LOG", "data": message})

    async def broadcast_progress(self, percentage: int):
        """Progress Bar ko update karne ke liye"""
        for connection in self.active_connections:
            await connection.send_json({"type": "PROGRESS", "data": percentage})

manager = ConnectionManager()

@router.websocket("/ws/migration/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: int):
    await manager.connect(websocket)
    try:
        # Welcome message jab user connect ho
        await websocket.send_json({"type": "INFO", "data": f"Connected to Stream: Job #{job_id}"})
        while True:
            # Server yahan wait karega signals ka
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)