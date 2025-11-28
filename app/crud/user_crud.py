from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    hashed_pass = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_pass,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    db.add(db_user)
    await db.commit() 
    await db.refresh(db_user) 
    return db_user

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)

async def update_user_status(db: AsyncSession, user_id: int, is_active: bool) -> Optional[User]:
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(is_active=is_active)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()