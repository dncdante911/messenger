from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from app.models.key_bundle import KeyBundle
from app.schemas.key_schema import KeyBundleUpload

async def create_key_bundle(
    db: AsyncSession, 
    user_id: int, 
    key_data: KeyBundleUpload
) -> KeyBundle:
    db_key_bundle = KeyBundle(
        user_id=user_id,
        device_id=key_data.device_id,
        identity_key=key_data.identity_key,
        signed_pre_key=key_data.signed_pre_key,
        signature=key_data.signature
    )
    db.add(db_key_bundle)
    await db.commit() 
    await db.refresh(db_key_bundle) 
    return db_key_bundle

async def get_key_bundles_by_user(db: AsyncSession, user_id: int) -> List[KeyBundle]:
    stmt = select(KeyBundle).where(KeyBundle.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_key_bundle_by_device(db: AsyncSession, user_id: int, device_id: str) -> Optional[KeyBundle]:
    stmt = select(KeyBundle).where(
        (KeyBundle.user_id == user_id) & 
        (KeyBundle.device_id == device_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_key_bundle(
    db: AsyncSession, 
    bundle_id: int, 
    key_data: KeyBundleUpload
) -> Optional[KeyBundle]:
    update_data = key_data.model_dump(exclude_unset=True, exclude={'device_id'}) 
    
    stmt = (
        update(KeyBundle)
        .where(KeyBundle.id == bundle_id)
        .values(**update_data)
        .returning(KeyBundle)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()