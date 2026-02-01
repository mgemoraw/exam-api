from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class NewsBase(BaseModel):
    title: str
    content: str

class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    title: Optional[str] = None
    content: Optional[str] = None


class NewsResponse(NewsBase):
    id: UUID | str
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)
