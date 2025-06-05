from sqlalchemy.orm import Session
from app.infrastructure.repositories.tag_repository import TagRepository
from app.application.schemas.tag_dto import TagDTO

class TagService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TagRepository(db)

    def list_tags(self) -> list[TagDTO]:
        return self.repository.list()

    def get_tag(self, tag_id: int) -> TagDTO:
        return self.repository.get(tag_id)

    def create_tag(self, name: str) -> TagDTO:
        return self.repository.create(name)

    def update_tag(self, tag_id: int, name: str) -> TagDTO:
        return self.repository.update(tag_id, name)

    def delete_tag(self, tag_id: int) -> None:
        self.repository.delete(tag_id)
