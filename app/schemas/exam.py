from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4, UUID
from enum import Enum

class ExamRequest(BaseModel):
    pass 

class ExamTypeEnum(Enum):
    MODEL_EXIT_EXAM ="model exit exam"
    HOLISTIC_EXAM="holistic exam"
    ENTRANCE_EXAM="entrance exam"

class ExamCreateRequest (BaseModel):
    id: UUID
    duration_minutes: int 
    maximum_marks: int 
    exam_type: Optional[Enum]=ExamTypeEnum.MODEL_EXIT_EXAM    
    class Config:
        from_attributes=True


class ExamResponse (BaseModel):
    id: UUID
    duration_minutes: int 
    maximum_marks: int 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True

