# app/modules/user/service.py

from app.modules.user.repository import UserRepository
from app.modules.user.models import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_data):
        existing = self.repo.get_by_email(user_data["email"])
        if existing:
            raise ValueError("Email already registered")

        user = User(**user_data)
        return self.repo.create(user)

    def update_user(self, user_id: str, update_data):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repo.create(user)  # reuse commit logic

    def delete_user(self, user_id: str):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        self.repo.delete(user)
        return True