from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
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

    def set_categories(self, item: Item, category_ids: list[int]) -> Item:
        # List all categories with given IDs
        categories = (
            self.db.query(Category)
            .filter(Category.id.in_(category_ids))
            .all()
        )

        if len(categories) != len(category_ids):
            raise ValueError("Some categories don't exist")

        # Associer les catégories à l'item
        item.categories = categories

        self.db.commit()
        self.db.refresh(item)
        return item
    
    def set_tags(self, item: Item, tag_names: list[str]) -> Item:
        # List to store tags
        tags = []

        for name in tag_names:
            # Search for the tag
            tag = self.db.query(Tag).filter(Tag.name == name).first()

            if not tag:
                # If tag doesn't exist create it
                tag = Tag(name=name)
                self.db.add(tag)
                self.db.flush()  # flush() to get ID without commit

            tags.append(tag)

        # Associate tags with item
        item.tags = tags

        self.db.commit()
        self.db.refresh(item)
        return item
    
    def list(self) -> List[Item]:
        return self.db.query(Item).all()
    
    def list_with_stats(
        self,
        category_id: Optional[int] = None,
        tag_names: Optional[List[str]] = None
    ):
        q = (
            self.db.query(
                Item,
                func.coalesce(func.avg(Rating.value), 0).label("avg_rating"),
                func.count(Rating.id).label("count_rating")
            )
            .outerjoin(Item.ratings)
            .options(joinedload(Item.categories))
            .options(joinedload(Item.tags))
        )

        # Filtrer par catégorie si demandé
        if category_id is not None:
            q = (
                q.join(Item.categories)
                 .filter(Category.id == category_id)
            )

        # Filtrer par tags si demandé
        if tag_names:
            q = (
                q.join(Item.tags)
                 .filter(Tag.name.in_(tag_names))
            )

        return (
            q.group_by(Item.id)
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
