from sqlalchemy import URL, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.domain.base import Base  # Importer Base depuis le fichier commun
import app.domain  # Ceci charge les modules user, item, rating via __init__.py
from app.config import settings
from app.infrastructure.seeders.category_seeder import seed_categories
from app.infrastructure.seeders.item_seeder import seed_items
import os

# Check if we're running in test mode
is_test = os.environ.get("APP_ENV") == "test"

# Use SQLite for tests, PostgreSQL for production
if is_test:
    from app.config_test import test_settings
    SQLALCHEMY_DATABASE_URL = test_settings.DATABASE_URL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Only needed for SQLite
    )
else:
    if(settings.DB_ENGINE == "postgresql"):
        url = URL.create(
            drivername="postgresql",
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            database=settings.DB_NAME
        )

        engine = create_engine(url) 
    else:
        DATABASE_URL = f"{settings.DB_ENGINE}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        engine = create_engine(
            DATABASE_URL, 
            connect_args={"check_same_thread": False}
        )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def drop_all_except_users(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    tables_to_drop = [t for t in tables if t != "users"]
    if tables_to_drop:
        Base.metadata.drop_all(bind=engine, tables=[Base.metadata.tables[t] for t in tables_to_drop])


def init_db():
    if(settings.APP_DEBUG):
        Base.metadata.drop_all(bind=engine) # only in dev
        print("DEBUG: flushing db")
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer les tables au démarrage
init_db()

if(settings.APP_DEBUG):
    # Créer une session temporaire pour exécuter le seeder
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_items(db)
    finally:
        db.close()