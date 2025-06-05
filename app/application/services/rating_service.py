# app/application/services/rating_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.rating import Rating
from app.infrastructure.repositories.rating_repository import RatingRepository
from app.application.schemas.rating_dto import RatingCreateDTO, RatingUpdateDTO

class RatingService:
    def __init__(self, db_session: Session):
        self.repository = RatingRepository(db_session)

    def get_user_rating_for_item(self, user_id: int, item_id: int) -> Rating:
        rating = self.repository.get_by_user_and_item(user_id, item_id)
        if not rating:
            raise ValueError("Rating not found")
        return rating
    
    def create_rating(self, dto: RatingCreateDTO) -> Rating:
        # 1) check duplicate
        existing = self.repository.get_by_user_and_item(dto.user_id, dto.item_id)
        if existing:
            raise ValueError("You have already rated this item.")
        # 2) create new
        return self.repository.create(dto)

    def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        return self.repository.get_by_id(rating_id)
    
    def get_ratings_by_item_id(self, item_id: int) -> list:
        return self.repository.get_ratings_by_item_id(item_id)

    def list_ratings(self) -> List[Rating]:
        return self.repository.list()
    
    def list_user_ratings(self, user_id: int) -> list:
        return self.repository.get_ratings_by_user_id(user_id)

    def update_rating(self, rating_id: int, rating_data: RatingUpdateDTO) -> Optional[Rating]:
        return self.repository.update(rating_id, rating_data)

    def delete_rating(self, rating_id: int) -> bool:
        return self.repository.delete(rating_id)

    def remove_comment(self, rating_id: int):
        """
        Remove the comment from a rating without affecting the score
        
        Args:
            rating_id: ID of the rating to modify
            
        Returns:
            The updated rating or None if not found
        """
        rating = self.repository.get_by_id(rating_id)
        if not rating:
            return None
            
        # Remove the comment but keep the score
        rating.comment = None
        self.repository.update(rating)
        
        return rating
