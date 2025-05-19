from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.base import Base  # Importer Base depuis le fichier commun
import app.domain  # Ceci charge les modules user, item, rating via __init__.py
from app.config import settings
from app.infrastructure.seeders.category_seeder import seed_categories
from app.infrastructure.seeders.item_seeder import seed_items

if(settings.APP_DEBUG):
    DATABASE_URL = "sqlite:///./ratings.db"
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
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