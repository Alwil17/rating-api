from app.infrastructure.database import SessionLocal
from app.infrastructure.seeders.category_seeder import seed_categories
from app.infrastructure.seeders.item_seeder import seed_items

db = SessionLocal()
seed_categories(db)
seed_items(db)
db.close()
