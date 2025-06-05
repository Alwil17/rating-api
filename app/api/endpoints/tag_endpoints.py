from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.application.schemas.tag_dto import TagDTO, TagCreateDTO, TagUpdateDTO
from app.application.services.tag_service import TagService
from app.infrastructure.database import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("", response_model=list[TagDTO])
def list_tags(db: Session = Depends(get_db)):
    return TagService(db).list_tags()

@router.post("", response_model=TagDTO, status_code=201)
def create_tag(tag: TagCreateDTO, db: Session = Depends(get_db)):
    return TagService(db).create_tag(tag.name)

@router.get("/{tag_id}", response_model=TagDTO)
def get_tag(
    tag_id: int = Path(..., title="The ID of the tag to get"),
    db: Session = Depends(get_db)
):
    tag = TagService(db).get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=TagDTO)
def update_tag(
    tag: TagUpdateDTO,
    tag_id: int = Path(..., title="The ID of the tag to update"),
    db: Session = Depends(get_db)
):
    result = TagService(db).get_tag(tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagService(db).update_tag(tag_id, tag.name)

@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int = Path(..., title="The ID of the tag to delete"),
    db: Session = Depends(get_db)
):
    tag = TagService(db).get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    TagService(db).delete_tag(tag_id)
    return None
