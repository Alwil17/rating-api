from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.category import Category
from app.domain.item import Item
from app.application.schemas.item_dto import ItemCreateDTO, ItemUpdateDTO
from app.domain.rating import Rating
from app.domain.tag import Tag

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item_data: ItemCreateDTO) -> Item:
        item = Item(**item_data.dict())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == item_id).first()
    
    def get_with_stats(self, item_id: int) -> Optional[Item]:
        return (
            self.db.query(
                Item,
                func.coalesce(func.avg(Rating.value), 0).label("avg_rating"),
                func.count(Rating.id).label("count_rating")
            )
            .outerjoin(Item.ratings)
            .filter(Item.id == item_id)
            .group_by(Item.id)
            .first()
        )

    def set_categories(self, item: Item, category_ids: list[int]):
        item.categories = self.db.query(Category).filter(Category.id.in_(category_ids)).all()
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def set_tags(self, item: Item, tag_names: list[str]):
        tags = [self.db.query(Tag).filter(Tag.name == name).first() or Tag(name=name) for name in tag_names]
        item.tags = tags
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def list(self) -> List[Item]:
        return self.db.query(Item).all()
    
    def list_with_stats(self):
        # SELECT items.*, AVG(ratings.value) AS avg_rating, COUNT(ratings.id) AS count_rating
        return (
            self.db.query(
                Item,
                func.coalesce(func.avg(Rating.value), 0).label("avg_rating"),
                func.count(Rating.id).label("count_rating")
            )
            .outerjoin(Item.ratings)  # jointure sur ratings
            .group_by(Item.id)
            .all()
        )

    def update(self, item_id: int, item_data: ItemUpdateDTO) -> Optional[Item]:
        item = self.get_by_id(item_id)
        if not item:
            return None
        update_data = item_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get_by_id(item_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
