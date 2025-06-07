from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.api.security import hash_password
from app.domain.user import User
from app.domain.rating import Rating
from app.application.schemas.user_dto import (
    UserCreateDTO, UserUpdateDTO, 
    UserGrowthDTO, UserEngagementDTO, UserStatsDTO
)
from app.config import settings

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreateDTO) -> User:
        hashed_pw = hash_password(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_pw
        )

        if(settings.APP_DEBUG and ("admin" in user_data.email)):
            user.role = "admin"

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def list(self) -> List[User]:
        return self.db.query(User).all()

    def update(self, user_id: int, user_data: UserUpdateDTO) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        update_data = user_data.model_dump(exclude_unset=True)
        # Hash the password if present
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def get_user_growth(self, days: int = 30) -> List[UserGrowthDTO]:
        """
        Get user growth data for the specified number of days
        Shows the number of new users that registered each day
        """
        # Calculate the start date (n days ago)
        start_date = datetime.now() - timedelta(days=days)
        
        # Query to get count of users registered per day
        results = self.db.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        ).filter(
            User.created_at >= start_date
        ).group_by(
            func.date(User.created_at)
        ).order_by(
            'date'
        ).all()
        
        # Create a dictionary with all dates in the range
        all_dates = {}
        current_date = start_date.date()
        end_date = datetime.now().date()
        
        while current_date <= end_date:
            all_dates[current_date] = 0
            current_date += timedelta(days=1)
        
        # Fill in the actual counts
        for date_count in results:
            all_dates[date_count.date] = date_count.count
        
        # Convert to the DTO format
        return [
            UserGrowthDTO(date=date, count=count)
            for date, count in all_dates.items()
        ]

    def get_user_engagement(self, limit: int = 10) -> List[UserEngagementDTO]:
        """
        Get most engaged users based on rating activity
        """
        results = self.db.query(
            User.id.label('user_id'),
            User.name.label('username'),
            func.count(Rating.id).label('ratings_count'),
            func.max(Rating.created_at).label('last_activity')
        ).join(
            Rating, User.id == Rating.user_id
        ).group_by(
            User.id, User.name
        ).order_by(
            desc('ratings_count')
        ).limit(limit).all()
        
        return [
            UserEngagementDTO(
                user_id=r.user_id,
                username=r.username,
                ratings_count=r.ratings_count,
                last_activity=r.last_activity.date()
            )
            for r in results
        ]

    def get_user_stats(self) -> UserStatsDTO:
        """
        Get overall user statistics
        """
        # Total users
        total_users = self.db.query(func.count(User.id)).scalar() or 0
        
        # Active users (users with at least one rating in last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_users = self.db.query(
            func.count(func.distinct(Rating.user_id))
        ).filter(
            Rating.created_at >= thirty_days_ago
        ).scalar() or 0
        
        # New users today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        new_users_today = self.db.query(
            func.count(User.id)
        ).filter(
            User.created_at >= today_start
        ).scalar() or 0
        
        # Average ratings per user - fixed to use a subquery approach
        # First, get count of ratings per user in a subquery
        from sqlalchemy import select
        subquery = select(
            Rating.user_id, 
            func.count(Rating.id).label('rating_count')
        ).group_by(Rating.user_id).subquery()
        
        # Then get the average of those counts
        avg_result = self.db.query(
            func.avg(subquery.c.rating_count)
        ).scalar() or 0
        
        return UserStatsDTO(
            total_users=total_users,
            active_users=active_users,
            new_users_today=new_users_today,
            average_ratings_per_user=round(float(avg_result), 1)
        )
