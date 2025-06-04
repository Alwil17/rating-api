from app.infrastructure.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db_session):
        self.repo = CategoryRepository(db_session)

    def list_categories(self):
        return self.repo.list()

    def create_category(self, name: str):
        return self.repo.create(name)
    
    # Get a specific category by ID
    def get_category(self, category_id: int):
        return self.repo.get(category_id)
    
    # Update a category
    def update_category(self, category_id: int, name: str = None, description: str = None):
        category = self.repo.get(category_id)
        if not category:
            return None
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
            
        return self.repo.update(category_id, update_data)
    
    # Delete a category
    def delete_category(self, category_id: int):
        return self.repo.delete(category_id)