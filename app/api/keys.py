from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User 
from app.schemas.key_schema import KeyBundleUpload, KeyBundlePublic
from app.crud import key_crud 

router = APIRouter(
    prefix="/keys",
    tags=["Key Management"],
)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_key_bundle(
    key_data: KeyBundleUpload,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    existing_bundle = await key_crud.get_key_bundle_by_device(
        db, 
        current_user.id, 
        key_data.device_id
    )
    
    if existing_bundle:
        await key_crud.update_key_bundle(db, existing_bundle.id, key_data)
        return {"message": "Key bundle updated successfully"}
    else:
        await key_crud.create_key_bundle(db, current_user.id, key_data)
        return {"message": "Key bundle created successfully"}

@router.get("/{user_id}", response_model=List[KeyBundlePublic])
async def get_user_keys(
    user_id: int,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot request own keys via this endpoint"
        )
        
    key_bundles = await key_crud.get_key_bundles_by_user(db, user_id)
    
    if not key_bundles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Public keys for this user not found. User must login first."
        )
        
    return key_bundles