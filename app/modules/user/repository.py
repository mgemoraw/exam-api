# app/modules/user/repository.py

# from app.modules.user.models import User
from app.models.user import User

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_by_email(self, email: str):
        user = self.db.query(User).filter(User.email==email).first()
        return user 

    def get_by_id(self, user_id: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()