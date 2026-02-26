from typing import Dict, TypeVar, Generic, Type, Optional, List, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from app.infrastructure.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_in: ModelType) -> ModelType:
        """Prepare a new record (No commit here - Service handles it)."""
        self.db.add(obj_in)
        return obj_in
    
    def update(self, db_obj: ModelType, obj_in: Union[ModelType, Dict[str, Any]]) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # For Pydantic models/objects
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        self.db.add(db_obj)
        return db_obj

    def get(self, id: Any) -> Optional[ModelType]:
        """Fetch a single record by its Primary Key."""
        return self.db.get(self.model, id)
        # return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, skip:int=0, limit:int=100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        return self.db.query(self.model).all()
    
    def remove(self, id: Any) -> Optional[ModelType]:
        """Delete a record."""
        obj = self.db.get(self.model, id)
        if obj:
            self.db.delete(obj)
        return obj
    
    
