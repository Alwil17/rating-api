from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.api.security import require_role
from app.application.schemas.item_dto import ItemResponse
from app.application.schemas.rating_dto import RatingResponse
from app.application.schemas.user_dto import UserCreateDTO, UserUpdateDTO, UserResponse
from app.application.services.rating_service import RatingService
from app.application.services.user_service import UserService
from app.domain.item import Item
from app.domain.rating import Rating
from app.infrastructure.database import get_db
from app.api.security import oauth2_scheme, require_role, verify_token

router = APIRouter(prefix="/users", tags=["Users"])

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
    if(user_id != current_user.id):
        raise HTTPException(status_code=404, detail="User don't match")
    rating_service = RatingService(db)
    return rating_service.list_user_ratings(current_user.id)

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
def update_user(user_id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
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
