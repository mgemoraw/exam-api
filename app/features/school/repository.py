

from sqlalchemy.orm import Session 
from app.core.base_repo import BaseRepository
from .models import (
    University,
)
from typing import Optional



class UniversityRepository(BaseRepository[University]):
    def __init__(self, db:Session):
        super().__init__(University, db)

    def get_by_code(self, code: str) -> Optional[University]:
        return self.db.query(self.model).filter(self.model.code == code).first()

    def get_by_name(self, name: str) -> Optional[University]:
        return self.db.query(self.model).filter(self.model.name == name).first()
   
    
