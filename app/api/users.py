from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.crud import user_crud
from app.models.user import User 
from app.schemas.user_schema import UserPublic

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: User = Depends(get_current_user) 
):
    return current_user 

@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user