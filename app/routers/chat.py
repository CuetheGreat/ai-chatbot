from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

connected_clients: set[WebSocket] = set()


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        await websocket.close()
