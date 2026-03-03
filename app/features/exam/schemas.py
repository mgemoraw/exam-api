from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal, Optional, List, Dict
from uuid import uuid4, UUID
from enum import Enum
from app.models.exam import ExamTypeEnum

class ExamRequest(BaseModel):
    pass 


class ExamCreateRequest(BaseModel):
    title: str
    program: str
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
    id: UUID | str
    title: str
    program: str
    maximum_marks: int
    duration_minutes: int
    exam_type: ExamTypeEnum
    description: Optional[str]
    is_visible: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    questions: Optional[List['ExamQuestionResponse']] = None
    model_config=ConfigDict(from_attributes=True)


class ExamQuestionResponse(BaseModel):
    id: UUID | str
    question: 'QuestionResponse'
    model_config=ConfigDict(from_attributes=True)

class QuestionResponse(BaseModel):
    id: UUID | str
    department: str
    course: str
    module: str
    question: List['ContentBlock']
    options: Dict[str, 'OptionBlock']   # {"A": OptionBlock(...), "B": ...}
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


class AnswerSubmitRequest(BaseModel):
    question_id: UUID
    selected_option: str


class ExamQuestionItem(BaseModel):
    question_id: UUID
    order: Optional[int] = Field(None, ge=1)
    marks_override: Optional[float] = Field(None, ge=0)


class AddQuestionsRequest(BaseModel):
    questions: List[ExamQuestionItem]

    @field_validator("questions")
    @classmethod
    def validate_unique_questions(cls, value):
        ids = [q.question_id for q in value]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate question IDs are not allowed")
        return value