from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.application.services.category_service import CategoryService
from app.application.schemas.category_dto import CategoryDTO, CategoryCreateDTO, CategoryUpdateDTO
from app.infrastructure.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=list[CategoryDTO])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService(db).list_categories()

@router.post("", response_model=CategoryDTO, status_code=201)
def create_category(category: CategoryCreateDTO, db: Session = Depends(get_db)):
    return CategoryService(db).create_category(category.name, category.description)

@router.get("/{category_id}", response_model=CategoryDTO)
def get_category(
    category_id: int = Path(..., title="The ID of the category to get"),
    db: Session = Depends(get_db)
):
    category = CategoryService(db).get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryDTO)
def update_category(
    category: CategoryUpdateDTO,
    category_id: int = Path(..., title="The ID of the category to update"),
    db: Session = Depends(get_db)
):
    result = CategoryService(db).get_category(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryService(db).update_category(category_id, category.name, category.description)

@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int = Path(..., title="The ID of the category to delete"),
    db: Session = Depends(get_db)
):
    category = CategoryService(db).get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    CategoryService(db).delete_category(category_id)
    return None

