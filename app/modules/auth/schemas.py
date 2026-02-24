from pydantic import ConfigDict
from ..app_base_model import AppBaseModel


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

