
from sqlalchemy.orm import Session
from .repo import QuestionRepository
from .models import Question, Option

from .schemas import MCQCreateRequest

class QuestionService:
    def __init__(self, db: Session):
        self.repo = QuestionRepository(db)

        self.db = db

    def get_question(self, id:str):
        return self.repo.get(id)
    

    def create_question(self, question: MCQCreateRequest) -> Question:
        pass 
