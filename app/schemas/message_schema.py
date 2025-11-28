from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

# Схема для команды, которую клиент отправляет по WebSocket
class WSCommand(BaseModel):
    type: str = Field(..., description="Тип команды: SEND_MSG, TYPING, READ")
    payload: Any = Field(..., description="Полезная нагрузка команды")

# Схема для полезной нагрузки команды SEND_MSG
class WSMessagePayload(BaseModel):
    recipient_id: int
    content: str # Зашифрованный контент

# Схема для исходящего сообщения (сервер -> клиент)
class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    timestamp: datetime