import asyncio
import json
from datetime import datetime
import websockets
import threading

async def connect_to_server():
    uri = "ws://172.16.111.76:8007/ws/root/"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                raw_response = await websocket.recv()
                response = json.loads(raw_response)

                response_thread = threading.Thread(target=share_response, args=(websocket, response))
                response_thread.start()


    except websockets.exceptions.ConnectionClosedError:
        print("Connection to server closed unexpectedly. Reconnecting...")
        await asyncio.sleep(1)  # Wait before attempting to reconnect

def share_response(websocket, response):
    asyncio.set_event_loop(asyncio.new_event_loop())  # Create new event loop for the thread
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_share_response(websocket, response))

async def _share_response(websocket, response):
    response["message"] = ai_response(response.get("message"))
    response["status"] = "SUCCESSFUL"
    await websocket.send(json.dumps(response))

def ai_response(message):
    if message != "You are now connected as a root user.":
        print(message)
        return message.upper()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(connect_to_server())

