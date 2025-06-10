from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from pydantic import conlist
from sqlalchemy.orm import Session
from app.application.schemas.item_dto import ItemCreateDTO, ItemUpdateDTO, ItemResponse
from app.application.schemas.rating_dto import RatingResponse
from app.application.services.item_service import ItemService
from app.application.services.rating_service import RatingService
from app.infrastructure.database import get_db
from app.api.security import oauth2_scheme, require_role, verify_token

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemResponse, status_code=201)
def create_item(item_data: ItemCreateDTO, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Vérifie le token ; renvoie le nom d'utilisateur ou lève une exception
    verify_token(token)
    item_service = ItemService(db)
    item = item_service.create_item(item_data)
    return item

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item, avg, count = ItemService(db).get_item(item_id)
        return serialize_item(item, avg, count)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def serialize_item(item, avg, count):
    return ItemResponse.model_validate({
        k: v for k, v in vars(item).items() if not k.startswith('_')
    } | {
        "avg_rating": avg,
        "count_rating": count
    })

@router.get("", response_model=list[ItemResponse])
def list_items(
    category_id: Optional[int] = None,
    tags: Optional[List[str]] = Query(None, description="Filter by tag names"),
    db: Session = Depends(get_db)
):
    try:
        items = ItemService(db).list_items(category_id, tags)
        # items: List[Tuple[Item, avg, count]]
        return [serialize_item(item, avg, count) for item, avg, count in items]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint pour récupérer tous les ratings d’un item donné
@router.get("/{item_id}/ratings", response_model=list[RatingResponse])
def get_ratings_by_item(item_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["user"]))):
    verify_token(token)
    rating_service = RatingService(db)
    return rating_service.get_ratings_by_item_id(item_id)


@router.put("/{item_id}/categories", status_code=204)
def set_item_categories(
    item_id: int,
    category_ids: conlist(item_type=int, min_length=1),
    db: Session = Depends(get_db)
):
    try:
        ItemService(db).set_item_categories(item_id, category_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}/tags", status_code=204)
def set_item_tags(
    item_id: int,
    tag_names: list[str],
    db: Session = Depends(get_db)
):
    try:
        ItemService(db).set_item_tags(item_id, tag_names)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdateDTO, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
    item_service = ItemService(db)
    updated_item = item_service.update_item(item_id, item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), role: str = Depends(require_role(["admin"]))):
    verify_token(token)
    item_service = ItemService(db)
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
