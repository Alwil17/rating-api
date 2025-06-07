from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.api.security import require_role
from app.application.schemas.item_dto import ItemResponse
from app.application.schemas.rating_dto import RatingResponse
from app.application.schemas.user_dto import (
    UserCreateDTO, UserUpdateDTO, UserResponse, 
    UserGrowthDTO, UserEngagementDTO, UserStatsDTO
)
from app.application.services.rating_service import RatingService
from app.application.services.user_service import UserService
from app.domain.item import Item
from app.domain.rating import Rating
from app.infrastructure.database import get_db
from app.api.security import oauth2_scheme, require_role, verify_token

router = APIRouter(prefix="/users", tags=["Users"])

# Admin Analytics Endpoints - place these before path parameter routes
@router.get("/growth", response_model=list[UserGrowthDTO])
def get_user_growth(
    days: int = 30,
    db: Session = Depends(get_db), 
    role: str = Depends(require_role(["admin"]))
):
    """Get user growth data for the specified number of days

    Shows the number of new users that registered each day

    Requires the "admin" role.

    Args:
        days (int, optional): Number of days to show growth data for. Defaults to 30.
    """

    user_service = UserService(db)
    return user_service.get_user_growth(days)

@router.get("/engagement", response_model=list[UserEngagementDTO])
def get_user_engagement(
    limit: int = 10,
    db: Session = Depends(get_db), 
    role: str = Depends(require_role(["admin"]))
):
    """
    Retrieve a list of the most engaged users based on rating activity.

    Args:
        limit (int, optional): The maximum number of users to return. Defaults to 10.
        db (Session): Database session dependency.
        role (str): Role dependency, requires "admin" role to access.

    Returns:
        List[UserEngagementDTO]: A list of user engagement data transfer objects.
    """

    user_service = UserService(db)
    return user_service.get_user_engagement(limit)

@router.get("/stats", response_model=UserStatsDTO)
def get_user_stats(
    db: Session = Depends(get_db), 
    role: str = Depends(require_role(["admin"]))
):
    """Get overall user statistics

    Returns a dictionary with the following keys:
    
    - total_users: The total number of users in the database
    - total_items: The total number of items in the database
    - total_ratings: The total number of ratings in the database
    
    Requires the "admin" role.
    """
    user_service = UserService(db)
    return user_service.get_user_stats()

@router.post("", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db), role: str = Depends(require_role(["admin"]))):
    user_service = UserService(db)
    try:
        user = user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
    user_service = UserService(db)
    return user_service.list_users()

# Endpoint pour lister tous les ratings d'un user
@router.get("/{user_id}/ratings", response_model=list[RatingResponse])
def list_user_ratings(user_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    if(user_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=404, detail="User don't match")
    rating_service = RatingService(db)
    return rating_service.list_user_ratings(user_id)

@router.get("/{user_id}/recommandations", response_model=List[ItemResponse])
def get_recommandations(user_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    if(user_id != current_user.id):
        raise HTTPException(status_code=404, detail="User don't match")
    # Récupère les IDs des items déjà notés
    rated_item_ids = db.query(Rating.item_id).filter(Rating.user_id == user_id).subquery()

    # Sélectionne d'autres items (ex : les plus populaires ou récents)
    recommended_items = (
        db.query(Item)
        .filter(~Item.id.in_(rated_item_ids))
        .order_by(Item.created_at.desc())  # ou Item.popularity.desc() si dispo
        .limit(10)
        .all()
    )

    return recommended_items

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db), role: str = Depends(require_role(["admin"]))):
    user_service = UserService(db)
    updated_user = user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.put("/{user_id}/reset-password", response_model=dict)
def reset_user_password(
    password_data: dict,
    user_id: int = Path(..., title="The ID of the user to update password"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Reset a user's password (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Only administrators can reset passwords"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "password" not in password_data or not password_data["password"]:
        raise HTTPException(
            status_code=400, 
            detail="Password is required"
        )
    # Create a new UserUpdateDTO with the new password
    new_password = password_data.get("password")
    user_data = UserUpdateDTO(
        name=user.name,  # Keep the same name
        email=user.email,  # Keep the same email
        password=new_password,  # New password from request
        image_url=user.image_url,  # Keep the same image URL
        role=user.role  # Keep the same role
    )
    # Update with new password
    user_service.update_user(
        user_id=user_id, 
        user_data=user_data
    )
    
    return {"message": "Password reset successfully"}

