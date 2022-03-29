from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from asyncio import sleep, create_task

from get_information import get_banks
from connection_manager import ConnectionManager

DELAY = 300

app = FastAPI()
manager = ConnectionManager()

with open("main.html", "r") as file:
    HTML_page = file.read()


@app.get("/")
async def root():
    return HTMLResponse(HTML_page)


async def get_updates():
    while True:
        banks = get_banks()
        # отправляем каждому подключенному пользователю обновления по банкам
        for user in manager.active_connections:
            await user.send_text(banks)
        await sleep(DELAY)


# Функция общения вебсокета с клиентом в фоне
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)  # Принимаем подключение от пользователя
    try:
        while True:
            # Цикл для поддержки соединения, тк без него пользователь отключится
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# При старте приложения добавляем корутину get_updates() в цикл событий
@app.on_event("startup")
async def startup():
    create_task(get_updates())
