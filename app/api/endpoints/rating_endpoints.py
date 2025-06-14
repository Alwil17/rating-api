from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.endpoints.auth_endpoints import get_current_user
from app.application.schemas.rating_dto import (
    RatingCreateDTO, RatingUpdateDTO, RatingResponse,
    RatingDistributionDTO, RecentRatingDTO, RatingStatsDTO
)
from app.application.schemas.user_dto import UserResponse
from app.application.services.rating_service import RatingService
from app.infrastructure.database import get_db
from app.api.security import oauth2_scheme, require_role, verify_token

router = APIRouter(prefix="/ratings", tags=["Ratings"])

# Analytics Endpoints - moved to the top to avoid route conflicts
@router.get("/distribution", response_model=list[RatingDistributionDTO])
def get_rating_distribution(
    db: Session = Depends(get_db),
    role: str = Depends(require_role(["admin"]))
):
    rating_service = RatingService(db)
    return rating_service.get_rating_distribution()

@router.get("/recent", response_model=list[RecentRatingDTO])
def get_recent_ratings(
    limit: int = 10,
    db: Session = Depends(get_db), 
    role: str = Depends(require_role(["admin"]))
):
    rating_service = RatingService(db)
    return rating_service.get_recent_ratings(limit)

@router.get("/stats", response_model=RatingStatsDTO)
def get_rating_stats(
    db: Session = Depends(get_db), 
    role: str = Depends(require_role(["admin"]))
):
    rating_service = RatingService(db)
    return rating_service.get_rating_stats()

@router.get("/{item_id}/my-rating", response_model=RatingResponse)
def get_my_rating_for_item(
    item_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: UserResponse = Depends(get_current_user)
):
    verify_token(token)
    service = RatingService(db)
    try:
        rating = service.get_user_rating_for_item(current_user.id, item_id)
        return rating
    except ValueError:
        raise HTTPException(status_code=404, detail="No rating found for this item")
    
# Endpoint pour créer un nouveau rating
@router.post("", response_model=RatingResponse, status_code=201)
def create_rating(rating_dto: RatingCreateDTO, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["user"]))):
    verify_token(token)
    rating_service = RatingService(db)
    try:
        rating = rating_service.create_rating(rating_dto)
    except ValueError as e:
        # duplicate → 409 Conflict
        if "already rated" in str(e):
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )
        raise HTTPException(status_code=400, detail=str(e))
    return rating

# Endpoint pour récupérer un rating par ID
@router.get("/{rating_id}", response_model=RatingResponse)
def get_rating(rating_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    rating_service = RatingService(db)
    rating = rating_service.get_rating_by_id(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

# Endpoint pour lister tous les ratings
@router.get("", response_model=list[RatingResponse])
def list_ratings(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
    rating_service = RatingService(db)
    return rating_service.list_ratings()

# Endpoint pour mettre à jour un rating existant
@router.put("/{rating_id}", response_model=RatingResponse)
def update_rating(rating_id: int, rating_dto: RatingUpdateDTO, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["user"]))):
    verify_token(token)
    rating_service = RatingService(db)
    rating = rating_service.update_rating(rating_id, rating_dto)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

# Endpoint pour supprimer le commentaire d'un rating
@router.delete("/{rating_id}/comment", status_code=200, response_model=RatingResponse)
def remove_rating_comment(rating_id: int, db: Session = Depends(get_db), role: str = Depends(require_role(["admin"]))):
    rating_service = RatingService(db)
    rating = rating_service.remove_comment(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

# Endpoint pour supprimer un rating
@router.delete("/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: UserResponse = Depends(get_current_user)):
    verify_token(token)
    # Check if user own a rating
    rating = get_rating(rating_id=rating_id, db=db, token=token)
    if(current_user.id != rating.user_id):
        raise HTTPException(status_code=409, detail="This user is not the owner of specified rating")
    # Now proceed to deletion
    rating_service = RatingService(db)
    success = rating_service.delete_rating(rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return None
