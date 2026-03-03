from pydantic import BaseModel
from typing import Optional


class ChapterCreate(BaseModel):
    title: str


class NoteCreate(BaseModel):
    title: str
    content: str
    chapter_id: int
    is_published: bool = False


class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_published: Optional[bool]


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool

    class Config:
        orm_mode = True