import asyncio
import json
from datetime import datetime
import websockets
import threading
import queue

async def connect_to_server():
    uri = "ws://172.16.111.76:8007/ws/root/"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                raw_response = await websocket.recv()
                response = json.loads(raw_response)
                print(response)
                # server_thread = threading.Thread(target=_listen_to_server, args=(websocket,))
                # server_thread.start()

                # Start the thread for sharing responses
                response_thread = threading.Thread(target=share_response, args=(websocket, response))
                response_thread.start()

                # # Wait for both threads to finish
                # server_thread.join()
                # response_thread.join()

    except websockets.exceptions.ConnectionClosedError:
        print("Connection to server closed unexpectedly. Reconnecting...")
        await asyncio.sleep(1)  # Wait before attempting to reconnect
    

def listen_to_server(websocket):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_listen_to_server(websocket))

def _listen_to_server(websocket):
    while True:
        try:
            for message in websocket:
                print("Message received from server:", message)
                response_queue.put(message)  # Put received message into response queue
        except websockets.exceptions.ConnectionClosedError:
            print("Connection to server closed.")

def share_response(websocket, response):
    asyncio.set_event_loop(asyncio.new_event_loop())  # Create new event loop for the thread
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_share_response(websocket, response))

async def _share_response(websocket, response):
    print(response)
    response_message = ai_response(response.get("message"))
    response["message"] = "HELOOOOOO"
    await websocket.send(json.dumps(response))
    # while True:
    #     if not response_queue.empty():
    #         message = response_queue.get()  # Get message from response queue
    #         response_message = ai_response(message)
    #         response_data = {
    #             "message": response_message,
    #             "conversation_id": "123",
    #             "message_id": "456",
    #             "client_id": "789",
    #             "client_port": 12345,
    #             "time": int(datetime.now().timestamp() * 1000),
    #             "sender": "AI"
    #         }
    #         await websocket.send(json.dumps(response_data))
    #         print("Response sent to server:", response_data)

def ai_response(message):
    print("Received message:", message)
    return "AI processed: " + message.upper()

if __name__ == "__main__":
    response_queue = queue.Queue()  # Queue for storing server requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(connect_to_server())

