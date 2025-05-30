from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.domain.item import Item
from app.infrastructure.repositories.item_repository import ItemRepository
from app.application.schemas.item_dto import ItemCreateDTO, ItemUpdateDTO

class ItemService:
    def __init__(self, db_session: Session):
        self.repository = ItemRepository(db_session)

    def create_item(self, item_data: ItemCreateDTO) -> Item:
        # Créer l'item sans les relations
        item = self.repository.create(item_data)

        # Check if there are categories
        if item_data.category_ids:
            self.repository.set_categories(item, item_data.category_ids)

        # Check for tags
        if item_data.tags:
            self.repository.set_tags(item, item_data.tags)

        return item

    
    def get_item(self, item_id: int) -> Tuple[Item, float, int]:
        result = self.repository.get_with_stats(item_id)
        if not result:
            raise ValueError("Item not found")
        return result
    
    def list_items(
        self,
        category_id: Optional[int] = None,
        tag_names: Optional[List[str]] = None
    ) -> List[Tuple[Item, float, int]]:
        return self.repository.list_with_stats(category_id, tag_names)
    

    def update_item(self, item_id: int, item_data: ItemUpdateDTO) -> Optional[Item]:
        return self.repository.update(item_id, item_data)

    def delete_item(self, item_id: int) -> bool:
        return self.repository.delete(item_id)
    
    def set_item_categories(self, item_id: int, category_ids: list[int]):
        item = self.get_item(item_id)
        return self.repository.set_categories(item[0], category_ids)
    
    def set_item_tags(self, item_id: int, tag_names: list[str]):
        item = self.get_item(item_id)[0]
        return self.repository.set_tags(item, tag_names)
