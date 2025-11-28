from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.api import auth, keys, users 
from app.websocket.handlers import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 🚀 Инициализация: Запуск БД... ---")
    # await init_db() 
    print("--- ✅ Инициализация завершена. ---")
    yield
    print("--- 🛑 Приложение завершает работу. ---")


app = FastAPI(
    title="Tele-mess API",
    version="0.1.0",
    description="Backend API for real-time messaging application.",
    lifespan=lifespan 
)

# HTTP API
app.include_router(auth.router, prefix="/api/v1")
app.include_router(keys.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

# WebSocket API
app.include_router(ws_router) 


@app.get("/")
async def health_check():
    return {"status": "ok", "app": "Tele-mess is running"}


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=settings.WS_HOST, 
        port=settings.WS_PORT 
    )