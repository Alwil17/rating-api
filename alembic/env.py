import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Import Base from your SQLAlchemy setup
from app.infrastructure.database import Base

# Import all models so Alembic can detect them
# Import the Base class first
from app.domain.user import User
from app.domain.item import Item
from app.domain.category import Category  
from app.domain.tag import Tag
from app.domain.rating import Rating
from app.domain.refresh_token import RefreshToken

# This is the Alembic Config object
config = context.config

# Get database URL from environment variables
from app.config import settings

db_absolute_url = f"{settings.DB_ENGINE}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
database_url = os.environ.get("DATABASE_URL") or db_absolute_url
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
