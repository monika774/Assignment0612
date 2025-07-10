from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from jose import jwt, JWTError
from typing import List

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ws_router = APIRouter()
clients: List[WebSocket] = []

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token or not await verify_token(token):
        await websocket.close()
        return
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)