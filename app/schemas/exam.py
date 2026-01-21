from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4, UUID

class ExamRequest(BaseModel):
    pass 

class ExamCreateRequest (BaseModel):
    id: UUID
    duration_minutes: int 
    maximum_marks: int 

class ExamResponse (BaseModel):
    id: UUID
    duration_minutes: int 
    maximum_marks: int 
    created_at: datetime
    updated_at: datetime

