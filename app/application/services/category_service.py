from app.infrastructure.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db_session):
        self.repo = CategoryRepository(db_session)

    def list_categories(self):
        return self.repo.list()

    def create_category(self, name: str):
        return self.repo.create(name)