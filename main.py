import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sockets import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

@app.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!",websocket)
        
@app.get("/")
async def read_index():
    # Return the content of the index.html file
    return FileResponse("index.html")

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=5000, reload=True)