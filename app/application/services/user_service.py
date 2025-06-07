from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.api.security import verify_password
from app.domain.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.schemas.user_dto import UserCreateDTO, UserUpdateDTO

class UserService:
    def __init__(self, db_session: Session):
        self.repository = UserRepository(db_session)

    def create_user(self, user_data: UserCreateDTO) -> User:
        # Vérifier si l'email existe déjà
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Un utilisateur avec cet email existe déjà.")
        return self.repository.create(user_data)

    def get_user_by_email(self, email: str) -> User:
        return self.repository.get_by_email(email)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.repository.list()

    def update_user(self, user_id: int, user_data: UserUpdateDTO) -> Optional[User]:
        return self.repository.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)

    def get_user_growth(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get user growth data for the specified number of days"""
        return self.repository.get_user_growth(days)

    def get_user_engagement(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most engaged users based on rating activity"""
        return self.repository.get_user_engagement(limit)

    def get_user_stats(self) -> Dict[str, Any]:
        """Get overall user statistics"""
        return self.repository.get_user_stats()
