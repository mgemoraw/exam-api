
from .models import Question, Option
from app.core.base_repo import BaseRepository
from sqlalchemy.orm import Session


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db:Session):
        super().__init__(Question, db)

    