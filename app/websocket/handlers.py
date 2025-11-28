import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from app.websocket.connection_manager import manager
from app.websocket.dependencies import get_current_user_from_websocket
from app.models.user import User
from app.schemas.message_schema import WSCommand, WSMessagePayload
from app.crud import message_crud 
from app.core.database import AsyncSessionLocal
from app.schemas.message_schema import MessageOut

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: User = Depends(get_current_user_from_websocket) 
):
    if current_user is None:
        return # Соединение уже закрыто в зависимости

    user_id = current_user.id
    
    try:
        await manager.connect(user_id, websocket)
        
        async with AsyncSessionLocal() as db:
            await user_crud.update_user_status(db, user_id, is_active=True)
            await manager.broadcast_status(user_id, "online")
            
        while True:
            data = await websocket.receive_json()
            
            try:
                command = WSCommand(**data)
            except Exception as e:
                print(f"WS Command parsing error: {e}")
                continue 
            
            if command.type == "SEND_MSG":
                await handle_send_message(user_id, WSMessagePayload(**command.payload))
                
            elif command.type == "TYPING":
                # В идеале: проверить, что получатель активен и отправить ему
                recipient_id = command.payload.get("recipient_id") 
                if recipient_id:
                     await manager.send_personal_message(recipient_id, data)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        print(f"WS Unhandled Error for user {user_id}: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        async with AsyncSessionLocal() as db:
            await user_crud.update_user_status(db, user_id, is_active=False)
            await manager.broadcast_status(user_id, "offline")


async def handle_send_message(sender_id: int, payload: WSMessagePayload):
    async with AsyncSessionLocal() as db:
        new_message = await message_crud.create_message(
            db=db,
            sender_id=sender_id,
            recipient_id=payload.recipient_id,
            content=payload.content
        )
        
        response_payload = {
            "type": "NEW_MSG",
            "payload": MessageOut.model_validate(new_message).model_dump()
        }
        
        is_sent = await manager.send_personal_message(payload.recipient_id, response_payload)
        
        if is_sent:
            await message_crud.mark_as_delivered(db, new_message.id)