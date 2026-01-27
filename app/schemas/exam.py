from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4, UUID
from enum import Enum
from app.models.exam import ExamTypeEnum

class ExamRequest(BaseModel):
    pass 


class ExamCreateRequest(BaseModel):
    title: str
    maximum_marks: int = 100
    duration_minutes: int
    is_visible: bool = False
    exam_type: ExamTypeEnum = ExamTypeEnum.MODEL_EXIT_EXAM
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None



class ExamResponse(BaseModel):
    id: str
    title: str
    maximum_marks: int
    duration_minutes: int
    exam_type: ExamTypeEnum
    description: Optional[str]
    is_visible: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

