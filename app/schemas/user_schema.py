from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None 
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserInDBBase(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInDBBase
    
class UserPublic(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
    model_config = {"from_attributes": True}