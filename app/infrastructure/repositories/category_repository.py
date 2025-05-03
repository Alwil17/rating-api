from sqlalchemy.orm import Session
from app.domain.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(Category).all()

    def get(self, id: int):
        return self.db.query(Category).filter(Category.id == id).first()

    def create(self, name: str):
        cat = Category(name=name)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat
