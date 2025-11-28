from fastapi import WebSocket, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security
from app.crud.user_crud import get_user_by_id
from app.core.database import AsyncSessionLocal 
from app.models.user import User
from typing import Optional

async def get_current_user_from_websocket(
    websocket: WebSocket, 
    token: str = Query(...) 
) -> Optional[User]:
    
    payload = security.decode_token(token)
    
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired token")
        return None

    user_id = payload.get("sub")
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token missing user ID")
        return None

    async with AsyncSessionLocal() as db:
        user = await get_user_by_id(db, int(user_id))
        
        if user is None or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User not found or inactive")
            return None
            
        return user