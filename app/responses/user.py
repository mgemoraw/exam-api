from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="Bearer")

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True