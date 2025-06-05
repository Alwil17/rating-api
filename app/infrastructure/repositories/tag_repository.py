from sqlalchemy.orm import Session
from app.domain.tag import Tag

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(Tag).all()

    def get(self, tag_id: int):
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def create(self, name: str):
        tag = Tag(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag_id: int, name: str):
        tag = self.get(tag_id)
        if tag:
            tag.name = name
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def delete(self, tag_id: int):
        tag = self.get(tag_id)
        if tag:
            self.db.delete(tag)
            self.db.commit()
