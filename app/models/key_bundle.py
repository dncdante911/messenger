from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base 

class KeyBundle(Base):
    __tablename__ = "key_bundles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    user = relationship("User", back_populates="key_bundles")

    device_id = Column(String(50), index=True, nullable=False) 
    identity_key = Column(Text, nullable=False)
    signed_pre_key = Column(Text, nullable=False)
    signature = Column(Text, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'device_id', name='uq_user_device_key'),
    )