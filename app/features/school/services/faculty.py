from .base import BaseService
from ..repositories.faculty import FacultyRepository
from sqlalchemy.orm import Session 

class FacultyService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.repo = FacultyRepository(db)


    def create_faculty(self):
        pass