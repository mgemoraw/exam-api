from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid 

from app.infrastructure.database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda:str(uuid.uuid4()), 
        index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    creator: Mapped['User'] = relationship('User', back_populates='news_items', foreign_keys=[created_by])