from sqlalchemy.orm import Session
from .schemas import NoteCreate, NoteUpdate, ChapterCreate
from .repository import NoteRepository
from .models import Note, Chapter
from ..school.models import Course
from .exceptions import ChapterNotFoundError, NoteNotFoundError, NoteNotPublishedError, CourseNotFoundError



class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NoteRepository(db)

    def create_chapter(self, course_id: str, chapter: ChapterCreate):
        course = self.db.query(Course).filter(Course.id == course_id).first()

        if not course:
            raise CourseNotFoundError
            # raise HTTPException(status_code=404, detail="Course not found")
        
        new_chapter = Chapter(
            title=chapter.title,
            course=course_id,
        )
        self.db.add(new_chapter)
        self.db.commit()
        self.db.refresh(new_chapter)

        return new_chapter
        
    def create_note(self, chapter_id:str, note: NoteCreate):
        chapter = self.db.query(Chapter).filter(Chapter.id == note.chapter_id).first()

        if not chapter:
            raise ChapterNotFoundError
            # raise HTTPException(status_code=404, detail="Chapter not found")  
        

        new_note = Note(
            title = note.title,
            content=note.content,
            chapter_id=note.chapter_id,
            is_published=note.is_published,
        )

        return self.repo.create_note(new_note)
    

        