from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=8)
    class Config:
        from_attributes = True
