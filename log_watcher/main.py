import asyncio
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from services.log_reader import get_last_lines

app = FastAPI()
log_file_path = "services/sample.log"

@app.get("/")
async def get():
    last_lines = get_last_lines(log_file_path, 10)
    print(last_lines)
    return HTMLResponse(content=open("index.html", "r").read().replace("{{last_lines}}", last_lines), status_code=200)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/log")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to stream log file updates to connected clients.
    
    Establishes a WebSocket connection and continuously sends new log
    entries to all active connections.
    """
    await manager.connect(websocket)
    try:
        last_size = os.path.getsize(log_file_path)
        while True:
            await asyncio.sleep(1)
            current_size = os.path.getsize(log_file_path)
            # Check if the file size has increased
            if current_size > last_size:
                # Get the last 10 lines of the file
                last_lines = get_last_lines(log_file_path, 10)
                # Send the last 10 lines to all connected clients
                await manager.send_message(last_lines)
                # Update the last size
                last_size = current_size

    except WebSocketDisconnect:
        # Handle the WebSocket disconnection event
        manager.disconnect(websocket)
        