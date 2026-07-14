"""WebSocket - Real-time chat, notifications"""
import json
import asyncio
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
import jwt

from app.core.config import settings

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.online_users: Set[int] = set()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.online_users.add(user_id)
        await self.broadcast_presence(user_id, "online")

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        self.online_users.discard(user_id)

    async def send_personal(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                self.disconnect(user_id)

    async def broadcast(self, message: dict, exclude: int = None):
        for user_id, ws in self.active_connections.items():
            if user_id != exclude:
                try:
                    await ws.send_json(message)
                except:
                    self.disconnect(user_id)

    async def broadcast_presence(self, user_id: int, status: str):
        await self.broadcast({
            "type": "presence", "user_id": user_id, "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }, exclude=user_id)


manager = ConnectionManager()


@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=1008)
            return
    except:
        await websocket.close(code=1008)
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            if msg_type == "chat_message":
                await manager.broadcast({
                    "type": "new_message", "chat_id": data.get("chat_id"),
                    "sender_id": user_id, "content": data.get("content"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            elif msg_type == "typing":
                await manager.broadcast({
                    "type": "typing", "chat_id": data.get("chat_id"),
                    "user_id": user_id, "is_typing": data.get("is_typing", False)
                })
            elif msg_type == "ping":
                await manager.send_personal(user_id, {"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(user_id)
