import json
import asyncio
from typing import Dict, Set
from fastapi import WebSocket
from app.schemas.message_schema import MessageOut 

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.raw_connections: Set[WebSocket] = set()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id in self.active_connections:
             await self.active_connections[user_id].close(code=1000, reason="New connection opened.")

        self.active_connections[user_id] = websocket
        self.raw_connections.add(websocket)
        print(f"WS CONNECTED: User {user_id}. Total active: {len(self.active_connections)}")

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if websocket in self.raw_connections:
            self.raw_connections.remove(websocket)
        print(f"WS DISCONNECTED: User {user_id}. Total remaining: {len(self.active_connections)}")

    async def send_personal_message(self, user_id: int, data: Dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(data)
                return True
            except Exception as e:
                print(f"Error sending message to {user_id}: {e}")
                return False
        return False 

    async def broadcast_status(self, sender_id: int, message: str):
        data = {"type": "status", "sender_id": sender_id, "content": message}
        send_tasks = []
        for ws in self.raw_connections:
            if ws != self.active_connections.get(sender_id):
                 send_tasks.append(ws.send_json(data))
                 
        await asyncio.gather(*send_tasks, return_exceptions=True)

manager = ConnectionManager()