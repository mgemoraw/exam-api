from pydantic import ConfigDict, BaseModel, Field, EmailStr
from ..app_base_model import AppBaseModel
import uuid
from typing import Optional

class TokenCreate(AppBaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	expires_in: int
	refresh_expires_in: int

	model_config=ConfigDict(from_attributes=True)


class TokenResponse(AppBaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	expires_in: int
	refresh_expires_in: int

	model_config=ConfigDict(from_attributes=True)


class TokenRefreshRequest(AppBaseModel):
	refresh_token: str	


class UserTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="Bearer")
    expires_in: int
    refresh_expires_in: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
	id: uuid.UUID | str
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
	