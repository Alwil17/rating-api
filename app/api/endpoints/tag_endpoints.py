from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.schemas.tag_dto import TagDTO
from app.infrastructure.database import get_db
from app.infrastructure.repositories.tag_repository import TagRepository

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("", response_model=list[TagDTO])
def list_tags(db: Session = Depends(get_db)):
    return TagRepository(db).list()
