from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from typing import AsyncGenerator

Base = declarative_base() 

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False 
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        # Р”Р»СЏ РєРѕСЂСЂРµРєС‚РЅРѕРіРѕ СЃРѕР·РґР°РЅРёСЏ С‚Р°Р±Р»РёС† С‚СЂРµР±СѓРµС‚СЃСЏ РёРјРїРѕСЂС‚РёСЂРѕРІР°С‚СЊ РІСЃРµ РјРѕРґРµР»Рё
        from app.models import user, message, key_bundle 
        await conn.run_sync(Base.metadata.create_all)