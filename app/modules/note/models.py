from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base, MainModel 
import uuid
from datetime import datetime, timezone 



class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="chapters")
    notes = relationship("Note", back_populates="chapter", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chapter = relationship("Chapter", back_populates="notes")

