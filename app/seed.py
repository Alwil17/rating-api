from app.infrastructure.database import SessionLocal
from app.infrastructure.seeders.category_seeder import seed_categories

db = SessionLocal()
seed_categories(db)
db.close()
