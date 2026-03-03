"""
POST   /notes
PUT    /notes/{note_id}
DELETE /notes/{note_id}
GET    /chapters/{chapter_id}/notes
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .models import Note, Chapter
from .schemas import NoteCreate, NoteUpdate, NoteResponse
from app.infrastructure.database import get_db
from .services import NoteService




note_router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@note_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db:Session=Depends(get_db)):
    service = NoteService(db)
    return service.create_note(note)    
    



@note_router.put("/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):

    pass