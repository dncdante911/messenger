from pydantic import BaseModel
from datetime import datetime

class KeyBundleUpload(BaseModel):
    device_id: str 
    identity_key: str  
    signed_pre_key: str 
    signature: str     

class KeyBundlePublic(BaseModel):
    user_id: int
    device_id: str
    identity_key: str
    signed_pre_key: str
    signature: str
    updated_at: datetime
    model_config = {"from_attributes": True}