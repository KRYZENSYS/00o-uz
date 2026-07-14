"""WebSocket"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json, asyncio

router = APIRouter(prefix="/ws", tags=["websocket"])


class ConnectionManager:
    def __init__(self):
        self.active: Dict[int, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, user_id: int, ws: WebSocket):
        await ws.accept()
        async with self.lock:
            self.active.setdefault(user_id, set()).add(ws)

    async def disconnect(self, user_id: int, ws: WebSocket):
        async with self.lock:
            if user_id in self.active: self.active[user_id].discard(ws)
            if user_id in self.active and not self.active[user_id]: del self.active[user_id]

    async def send_personal(self, user_id: int, message: dict):
        if user_id in self.active:
            for ws in list(self.active[user_id]):
                try: await ws.send_json(message)
                except: pass

    async def broadcast(self, message: dict):
        for user_id in list(self.active.keys()):
            await self.send_personal(user_id, message)

    async def send_chat(self, from_id: int, to_id: int, message: dict):
        await self.send_personal(to_id, {**message, "from": from_id})
        await self.send_personal(from_id, message)

    def is_online(self, user_id: int) -> bool:
        return user_id in self.active and len(self.active[user_id]) > 0

    def online_users(self) -> int:
        return len(self.active)


manager = ConnectionManager()


@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        await manager.send_personal(user_id, {"type": "connected", "message": "WebSocket ulandi"})
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg.get("type") == "chat":
                    to_id = msg.get("to")
                    if to_id: await manager.send_chat(user_id, to_id, {"type": "chat", "content": msg.get("content", "")})
                elif msg.get("type") == "typing":
                    to_id = msg.get("to")
                    if to_id: await manager.send_personal(to_id, {"type": "typing", "from": user_id})
            except: pass
    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)
