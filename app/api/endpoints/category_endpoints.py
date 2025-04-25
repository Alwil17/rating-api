from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.services.category_service import CategoryService
from app.application.schemas.category_dto import CategoryDTO
from app.infrastructure.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryDTO])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService(db).list_categories()

@router.post("/", response_model=CategoryDTO, status_code=201)
def create_category(name: str, db: Session = Depends(get_db)):
    return CategoryService(db).create_category(name)
