# app/modules/user/service.py

from app.core.security import hash_password, is_password_strong
from app.core.logging import logger 
from .repository import UserRepository
from .models import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, data):
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        
        if not is_password_strong(data.password):
            raise ValueError("Password is not Strong. Password should conain at least one Caps Lock letter, one small letter, one digit and one symbol.")

        user = User(
			username=data.username, 
			email=data.email,
			is_superuser=data.is_superuser,
			hashed_password=hash_password(data.password)
			)
        
        # user = User(**data.dict())
        return self.repo.create(user)

    def update_user(self, user_id: str, update_data):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repo.update(user)  # reuse commit logic

    def delete_user(self, user_id: str):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        self.repo.delete(user)
        return True
    
    def update_password(self, user_id, new_password):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if not is_password_strong(new_password):
            raise ValueError("Password is not Strong. Password should conain at least one Caps Lock letter, one small letter, one digit and one symbol.")

        user.hashed_password = hash_password(new_password)
        self.repo.update(user)
        return True
