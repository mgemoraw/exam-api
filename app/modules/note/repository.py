
from .models import Note, Chapter
from sqlalchemy.orm import Session 



class NoteRepository:
    def __init__(self, db: Session):
        self.db = db    


    def create_note(self, note: Note):
        self.db.add(note)
        self.db.flush()

        return note