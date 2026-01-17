from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
# from sqlalchemy.dialects.postgresql import UUID

class UserCreate(BaseModel):
	id: UUID
	username: str
	email: Optional[EmailStr]
	is_superuser: Optional[bool] = False
	password: str


class UserResponse(BaseModel):
	id: UUID
	username: str
	email: Optional[EmailStr]
	is_superuser: bool
	is_active: bool

	class Config:
		orm_mode = True

class UserLogin(BaseModel):
	username: str
	password: str
	