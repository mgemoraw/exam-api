from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional, List, Dict
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

    # class Config:
    #     from_attributes = True
    model_config=ConfigDict(from_attributes=True)


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

    model_config=ConfigDict(from_attributes=True)

 


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FORMULA = "formula"

class ContentBlock(BaseModel):
    type: ContentType
    value: str   # text, image path/URL, or LaTeX formula

class OptionBlock(BaseModel):
    content: List[ContentBlock]
    is_answer: bool = False

class MCQCreateRequest(BaseModel):
    department: str
    course: str
    module: str
    question: List[ContentBlock]
    options: Dict[str, OptionBlock]   # {"A": OptionBlock(...), "B": ...}

    created_at: Optional[datetime]=datetime.utcnow()
    updated_at: Optional[datetime]=datetime.utcnow()