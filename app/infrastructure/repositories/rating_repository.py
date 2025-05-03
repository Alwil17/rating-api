from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.rating import Rating
from app.application.schemas.rating_dto import RatingCreateDTO, RatingUpdateDTO

class RatingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rating_data: RatingCreateDTO) -> Rating:
        # Crée une instance Rating à partir du DTO
        rating = Rating(**rating_data.dict())
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_by_id(self, rating_id: int) -> Optional[Rating]:
        return self.db.query(Rating).filter(Rating.id == rating_id).first()

    def get_ratings_by_item_id(self, item_id: int) -> List[Rating]:
        return self.db.query(Rating).filter(Rating.item_id == item_id).all()
    
    def list(self) -> List[Rating]:
        return self.db.query(Rating).all()

    def update(self, rating_id: int, rating_data: RatingUpdateDTO) -> Optional[Rating]:
        rating = self.get_by_id(rating_id)
        if not rating:
            return None
        update_data = rating_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(rating, key, value)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def delete(self, rating_id: int) -> bool:
        rating = self.get_by_id(rating_id)
        if not rating:
            return False
        self.db.delete(rating)
        self.db.commit()
        return True
