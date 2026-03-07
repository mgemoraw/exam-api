from app.core.base_repo import BaseRepository
from ..models import Faculty
from sqlalchemy.orm import Session
from typing import Optional



class FacultyRepository(BaseRepository[Faculty]):
    def __init__(self, db:Session):
        super().__init__(Faculty, db)

  
    def get_by_code(self, code: str) -> Optional[Faculty]:
        return self.db.query(self.model).filter(self.model.code == code).first()

    def get_by_name(self, name: str) -> Optional[Faculty]:
        return self.db.query(self.model).filter(self.model.name == name).first()