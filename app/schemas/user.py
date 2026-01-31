from datetime import datetime
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


class TokenResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	expires_in: int
	refresh_expires_in: int

	model_config=ConfigDict(from_attributes=True)


class TokenRefreshRequest(BaseModel):
	refresh_token: str	

class RoleCreate(BaseModel):
	name: str
	description: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)
	
class RoleResponse(BaseModel):
	id: UUID
	name: str
	description: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)

class PermissionCreate(BaseModel):
	name: str
	description: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)


class PermissionResponse(BaseModel):
	id: UUID
	name: str
	description: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)

class RolePermissionCreate(BaseModel):
	role_id: UUID
	permission_id: UUID

	model_config=ConfigDict(from_attributes=True)

class RolePermissionResponse(BaseModel):
	id: UUID
	role_id: UUID
	permission_id: UUID

	model_config=ConfigDict(from_attributes=True)

class UserRoleAssignRequest(BaseModel):
	user_id: UUID
	role_id: UUID

	model_config=ConfigDict(from_attributes=True)
class UserRoleResponse(BaseModel):
	id: UUID
	user_id: UUID
	role_id: UUID

	model_config=ConfigDict(from_attributes=True)

class UserUpdateRequest(BaseModel):
	username: Optional[str] = None
	email: Optional[EmailStr] = None
	is_active: Optional[bool] = None
	is_superuser: Optional[bool] = None
	password: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)

class UserResponseWithRoles(BaseModel):
	id: UUID
	username: str
	email: Optional[EmailStr]
	is_superuser: bool
	is_active: bool
	roles: Optional[list[RoleResponse]] = []

	model_config=ConfigDict(from_attributes=True)


class UserResponseWithPermissions(BaseModel):
	id: UUID
	username: str
	email: Optional[EmailStr]
	is_superuser: bool
	is_active: bool
	permissions: Optional[list[PermissionResponse]] = []

	model_config=ConfigDict(from_attributes=True)


class UserPasswordUpdateRequest(BaseModel):
	old_password: str
	new_password: str

	model_config=ConfigDict(from_attributes=True)

class UserPasswordResetRequest(BaseModel):
	email: EmailStr

	model_config=ConfigDict(from_attributes=True)

class UserPasswordResetConfirmRequest(BaseModel):
	reset_token: str
	new_password: str

	model_config=ConfigDict(from_attributes=True)


class UserActivateRequest(BaseModel):
	activation_token: str

	model_config=ConfigDict(from_attributes=True)

class UserDeactivateRequest(BaseModel):
	deactivation_token: str

	model_config=ConfigDict(from_attributes=True)

class UserProfileCreateRequest(BaseModel):
	fname: str
	mname: str
	lname: str 
	phone: Optional[str] = None
	address: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)

class UserProfileResponse(BaseModel):
	id: UUID
	user_id: UUID
	fname: str
	mname: str
	lname: str 
	phone_number: Optional[str] = None
	address: Optional[str] = None
	bio: Optional[str] = None
	avatar_url: Optional[str] = None
	location: Optional[str] = None
	website: Optional[str] = None
	birth_date: Optional[str] = None
	social_links: Optional[str] = None
	preferences: Optional[str] = None
	settings: Optional[str] = None
	created_at: datetime 
	updated_at: datetime


	model_config=ConfigDict(from_attributes=True)


class UserProfileUpdateRequest(BaseModel):
	fname: Optional[str] = None
	mname: Optional[str] = None
	lname: Optional[str] = None 
	phone_number: Optional[str] = None
	address: Optional[str] = None
	bio: Optional[str] = None
	avatar_url: Optional[str] = None
	location: Optional[str] = None
	website: Optional[str] = None
	birth_date: Optional[str] = None
	social_links: Optional[str] = None
	preferences: Optional[str] = None
	settings: Optional[str] = None

	model_config=ConfigDict(from_attributes=True)