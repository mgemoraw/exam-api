from pydantic import BaseModel, EmailStr, ConfigDict
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

	# class Config:
	# 	from_attributes = True
	model_config=ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
	username: str
	password: str
	

class TokenCreate(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	expires_in: int
	refresh_expires_in: int

	model_config=ConfigDict(from_attributes=True)