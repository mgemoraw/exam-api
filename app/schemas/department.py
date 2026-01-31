from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional, List, Dict
from uuid import uuid4, UUID
from enum import Enum
from app.models.exam import ExamTypeEnum



class DepartmentCreateRequest(BaseModel):
    name: str
    code: str

    model_config=ConfigDict(from_attributes=True)


class DepartmentResponse(BaseModel):
    id: UUID
    name: str
    code: str
    created_at: datetime
    updated_at: datetime

    model_config=ConfigDict(from_attributes=True)


class DepartmentUpdateRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

    model_config=ConfigDict(from_attributes=True)

