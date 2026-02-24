# app/models/token.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import uuid

from app.infrastructure.database import Base


class RefreshToken(Base):
    """Model for storing refresh tokens"""
    __tablename__ = "refresh_tokens"
    
    id = Column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    jti = Column(String(64), unique=True, index=True, nullable=False)  # JWT ID
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, )
    token_hash = Column(String(128), nullable=False)  # Hashed token for security
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    user: Mapped['User'] = relationship("User", back_populates="refresh_tokens")