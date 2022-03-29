from typing import List
from fastapi import WebSocket


# Класс, который следит за подключением/отключением новых клиентов-websocket
class ConnectionManager:
    def __init__(self):
        self.active_connections = []  # Создаем список активных клиентов (их вебсокетов)

    def init(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Принимаем соединение и добавляем в список
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
