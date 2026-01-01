# models/user.py
from sqlalchemy import String, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)