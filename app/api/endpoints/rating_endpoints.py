from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.schemas.rating_dto import RatingCreateDTO, RatingUpdateDTO, RatingResponse
from app.application.services.rating_service import RatingService
from app.infrastructure.database import get_db
from app.api.security import oauth2_scheme, require_role, verify_token

router = APIRouter(prefix="/ratings", tags=["Ratings"])


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
def list_ratings(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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

# Endpoint pour supprimer un rating
@router.delete("/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["user"]))):
    verify_token(token)
    rating_service = RatingService(db)
    success = rating_service.delete_rating(rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return None
