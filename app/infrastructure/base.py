import uuid
from datetime import datetime
from slugify import slugify
from sqlalchemy import String, DateTime, Boolean, event
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.sql import func

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass 



class MainModel:
    # -------------------------
    # UUID Primary Key
    # -------------------------
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    # -------------------------
    # Slug
    # -------------------------
    slug_source_field = "name"

    @declared_attr
    def slug(cls):
        return mapped_column(String(160), unique=True, index=True)

    # -------------------------
    # Timestamps
    # -------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # -------------------------
    # Soft Delete (optional)
    # -------------------------
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    # -------------------------
    # Slug Generator
    # -------------------------
    @classmethod
    def generate_slug(cls, target):
        source_value = getattr(target, cls.slug_source_field, None)
        if not source_value:
            return None
        return slugify(source_value)