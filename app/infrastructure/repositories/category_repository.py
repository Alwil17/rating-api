from sqlalchemy.orm import Session
from app.domain.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(Category).all()

    def get(self, id: int):
        return self.db.query(Category).filter(Category.id == id).first()

    def create(self, name: str, description: str = None):
        cat = Category(name=name, description=description)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat
        
    def update(self, id: int, update_data: dict):
        category = self.get(id)
        if category:
            for key, value in update_data.items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category
        
    def delete(self, id: int):
        category = self.get(id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False
