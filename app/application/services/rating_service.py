# app/application/services/rating_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.rating import Rating
from app.infrastructure.repositories.rating_repository import RatingRepository
from app.application.schemas.rating_dto import RatingCreateDTO, RatingUpdateDTO

class RatingService:
    def __init__(self, db_session: Session):
        self.repository = RatingRepository(db_session)

    def create_rating(self, rating_data: RatingCreateDTO) -> Rating:
        # Ajouter ici la logique métier spécifique, par exemple :
        # - Vérifier si l'utilisateur et l'item existent
        # - Vérifier si l'utilisateur a déjà noté cet item
        return self.repository.create(rating_data)

    def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        return self.repository.get_by_id(rating_id)
    
    def get_ratings_by_item_id(self, item_id: int) -> list:
        return self.repository.get_ratings_by_item_id(item_id)

    def list_ratings(self) -> List[Rating]:
        return self.repository.list()

    def update_rating(self, rating_id: int, rating_data: RatingUpdateDTO) -> Optional[Rating]:
        return self.repository.update(rating_id, rating_data)

    def delete_rating(self, rating_id: int) -> bool:
        return self.repository.delete(rating_id)
