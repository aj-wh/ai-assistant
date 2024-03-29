import asyncio
import json
from datetime import datetime
import websockets


async def connect_to_server():
    uri = "ws://172.16.111.76:8007/ws/root/"
    while True:  # Reconnect loop
        try:
            async with websockets.connect(uri) as websocket:
                async for message in websocket:
                    print("Message received from server:", message)
                    response_message = ai_response(message)
                    response_data = {
                        "message": response_message,
                        "conversation_id": "123",
                        "message_id": "456",
                        "client_id": "789",
                        "client_port": 12345,
                        "time": int(datetime.now().timestamp() * 1000),
                        "sender": "AI"
                    }
                    await websocket.send(json.dumps(response_data))
                    print("Response sent to server:", response_data)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection to server closed unexpectedly. Reconnecting...")
            await asyncio.sleep(1)

def ai_response(message):
    print(message)
    return message


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_to_server())

