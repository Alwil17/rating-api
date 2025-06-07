from typing import List, Optional, Dict, Any
from sqlalchemy import func, desc
from sqlalchemy.orm import Session, joinedload
from app.domain.rating import Rating
from app.domain.item import Item
from app.domain.user import User
from app.domain.category import Category
from app.application.schemas.rating_dto import (
    RatingCreateDTO, RatingUpdateDTO,
    RatingDistributionDTO, TopCategoryDTO, RatingStatsDTO
)

class RatingRepository:
    def __init__(self, db: Session):
        """
        Initialize RatingRepository

        Args:
            db (Session): The SQLAlchemy session
        """
        self.db = db

    def get_by_user_and_item(self, user_id: int, item_id: int) -> Rating | None:
        return (
            self.db.query(Rating)
               .filter(Rating.user_id == user_id,
                       Rating.item_id == item_id)
               .first()
        )
    
    def create(self, rating_data: RatingCreateDTO) -> Rating:
        # Crée une instance Rating à partir du DTO
        rating = Rating(**rating_data.model_dump())
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_by_id(self, rating_id: int) -> Optional[Rating]:
        return self.db.query(Rating).filter(Rating.id == rating_id).first()

    def get_ratings_by_item_id(self, item_id: int) -> List[Rating]:
        return self.db.query(Rating).filter(Rating.item_id == item_id).all()
    
    def get_ratings_by_user_id(self, user_id: int) -> List[Rating]:
        return self.db.query(Rating).filter(Rating.user_id == user_id).all()
    
    def list(self) -> List[Rating]:
        return self.db.query(Rating).all()

    def update(self, rating_id: int, rating_data: RatingUpdateDTO) -> Optional[Rating]:
        rating = self.get_by_id(rating_id)
        if not rating:
            return None
        update_data = rating_data.model_dump(exclude_unset=True)
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

    def get_rating_distribution(self) -> List[RatingDistributionDTO]:
        """
        Get distribution of ratings across values 1-5
        Returns a list with count for each rating value
        """
        results = self.db.query(
            Rating.value,
            func.count(Rating.id).label('count')
        ).group_by(Rating.value).all()
        
        # Make sure all values 1-5 are represented
        distribution_map = {r.value: r.count for r in results}
        
        distribution = []
        for value in range(1, 6):
            distribution.append(RatingDistributionDTO(
                value=value,
                count=distribution_map.get(value, 0)
            ))
            
        return distribution

    def get_recent_ratings(self, limit: int = 10) -> List[Any]:
        """
        Get most recent ratings with user and item information
        """
        results = self.db.query(
            Rating, Item.name.label('item_name'), User.name.label('user_name')
        ).join(
            Item, Rating.item_id == Item.id
        ).join(
            User, Rating.user_id == User.id
        ).order_by(
            desc(Rating.created_at)
        ).limit(limit).all()
        
        return [
            {
                'id': r.Rating.id,
                'value': r.Rating.value,
                'item_name': r.item_name,
                'user_name': r.user_name,
                'created_at': r.Rating.created_at
            }
            for r in results
        ]

    def get_rating_stats(self) -> Dict[str, Any]:
        """
        Get overall rating statistics
        """
        # Get average rating
        avg_result = self.db.query(func.avg(Rating.value)).scalar() or 0
        average = round(float(avg_result), 1)
        
        # Get total count
        total_count = self.db.query(func.count(Rating.id)).scalar() or 0
        
        # Get top category - using the many-to-many relationship 
        # between items and categories through the item_category table
        top_category_result = self.db.query(
            Category.name,
            func.count(Rating.id).label('rating_count')
        ).join(
            # Use the proper association table to join categories and items
            Item.categories
        ).join(
            Rating, Item.id == Rating.item_id
        ).group_by(
            Category.name
        ).order_by(
            desc('rating_count')
        ).first()
        
        top_category = {
            'name': top_category_result.name if top_category_result else "Uncategorized",
            'count': top_category_result.rating_count if top_category_result else 0
        }
        
        return RatingStatsDTO(
            average=average,
            totalCount=total_count,
            topCategory=TopCategoryDTO(**top_category)
        )
