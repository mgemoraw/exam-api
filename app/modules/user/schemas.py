from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional

from pydantic.alias_generators import to_camel  
from datetime import datetime
from app.modules.app_base_model import AppBaseModel
from uuid import UUID

class UserBase(AppBaseModel):
    email: EmailStr

    
class UserCreate(AppBaseModel):
	id: UUID | str
	username: str = Field(..., min_length=3, max_length=50)
	email: Optional[EmailStr]
	is_superuser: Optional[bool] = False
	password: str = Field(..., min_length=6)

# class UserCreate(UserBase):
#     username: str = Field(..., min_length=3, max_length=50)
#     password: str = Field(..., min_length=6)

class UserRead(UserBase):
    id: str
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: str

    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)

class PermissionRead(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True



