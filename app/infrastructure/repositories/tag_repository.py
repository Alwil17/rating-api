from sqlalchemy.orm import Session
from app.domain.tag import Tag

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str):
        return self.db.query(Tag).filter(Tag.name == name).first()

    def create(self, name: str):
        tag = Tag(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_or_create(self, name: str):
        tag = self.get_by_name(name)
        if tag:
            return tag
        return self.create(name)

    def list(self):
        return self.db.query(Tag).all()
