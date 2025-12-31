import asyncio

import websockets


async def test_websocket():
    uri = "ws://localhost:8000/api/chat"
    async with websockets.connect(uri) as ws:
        await ws.send("Hello from Python!")
        response = await ws.recv()
        print("Received:", response)


asyncio.run(test_websocket())
