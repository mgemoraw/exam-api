# pip install python-flugify
from sqlalchemy import Column, String, event
from sqlalchemy.orm import declared_attr, object_session
from sqlalchemy.exc import IntegrityError
from slugify import slugify


class SlugMixin:
    slug_source_field = "name"

    @declared_attr
    def slug(cls):
        return Column(String(150), unique=True, nullable=False, index=True)

    @classmethod
    def generate_slug(cls, target):
        source_value = getattr(target, cls.slug_source_field, None)
        if not source_value:
            return None

        return slugify(source_value)

 


@event.listens_for(SlugMixin, "before_insert", propagate=True)
def auto_generate_slug(mapper, connection, target):
    if not getattr(target, "slug", None):
        target.slug = target.generate_slug(target)


