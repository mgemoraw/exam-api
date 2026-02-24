from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Dict, List, Optional
from uuid import UUID



class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FORMULA = "formula"

class ContentBlock(BaseModel):
    type: ContentType
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, v):
        if not v.strip():
            raise ValueError("Content value cannot be empty")
        return v

class OptionCreateSchema(BaseModel):
    content: List[ContentBlock]
    is_answer: bool = False

class OptionResponseSchema(BaseModel):
    content: List[ContentBlock]



class MCQCreateRequest(BaseModel):
    department: str
    course: str
    module: str
    question: List[ContentBlock]
    options: Dict[str, OptionCreateSchema]   # {"A": OptionCreateSchema(...), "B": ...}

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @field_validator("options")
    @classmethod
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("At least two options required")

        correct_count = sum(1 for opt in v.values() if opt.is_answer)

        if correct_count != 1:
            raise ValueError("Exactly one correct answer required")

        return v

class QuestionResponse(BaseModel):
    id: UUID | str
    department: str
    course: str
    module: str
    question: List['ContentBlock']
    options: Dict[str, 'OptionResponseSchema']   # {"A": OptionResponseSchema(...), "B": ...}
    model_config=ConfigDict(from_attributes=True)


class OptionSchema(BaseModel):
    key: str
    text: str


class QuestionUploadSchema(BaseModel):
    content: str
    question_type: str
    marks: float = Field(..., ge=0)
    options: List[OptionSchema]
    correct_option: str

    @field_validator("correct_option")
    @classmethod
    def validate_correct_option(cls, value):
        if not value:
            raise ValueError("Correct option is required")
        return value


class QuestionUploadRequest(BaseModel):
    questions: List[QuestionUploadSchema]
