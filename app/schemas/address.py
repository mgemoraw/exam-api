from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class AddressCreateRequest(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

    model_config=ConfigDict(from_attributes=True)

class AddressResponse(BaseModel):
    id: UUID
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config=ConfigDict(from_attributes=True)