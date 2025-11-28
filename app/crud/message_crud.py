from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, or_
from typing import List, Optional
from datetime import datetime
from app.models.message import Message

async def create_message(
    db: AsyncSession, 
    sender_id: int,
    recipient_id: int,
    content: str
) -> Message:
    db_message = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content,
    )
    db.add(db_message)
    await db.commit() 
    await db.refresh(db_message) 
    return db_message

async def get_conversation_history(
    db: AsyncSession, 
    user_id_a: int, 
    user_id_b: int, 
    limit: int = 50, 
    skip: int = 0
) -> List[Message]:
    stmt = (
        select(Message)
        .where(or_(
            (Message.sender_id == user_id_a) & (Message.recipient_id == user_id_b),
            (Message.sender_id == user_id_b) & (Message.recipient_id == user_id_a)
        ))
        .order_by(Message.created_at.desc()) 
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def mark_as_delivered(db: AsyncSession, message_id: int) -> Optional[Message]:
    stmt = (
        update(Message)
        .where(Message.id == message_id)
        .values(delivered_at=datetime.utcnow())
        .returning(Message)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()