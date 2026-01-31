from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

import uuid
from .base import Base


class Address(Base):
    __tablename__ = "addresses"
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    zip_code = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with University
    university = relationship("University", back_populates="address")

    def __repr__(self):
        return f"<Address(street={self.street}, city={self.city}, state={self.state}, zip_code={self.zip_code}, country={self.country})>" 