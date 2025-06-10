import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.config import settings

def setup_test_database():
    """Create a test database if it doesn't exist."""
    test_db_name = f"{settings.DB_NAME}_test"
    
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if test database exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (test_db_name,))
    exists = cursor.fetchone()
    
    # Create test database if it doesn't exist
    if not exists:
        print(f"Creating test database: {test_db_name}")
        cursor.execute(f"CREATE DATABASE {test_db_name}")
        print(f"Test database {test_db_name} created successfully")
    else:
        print(f"Test database {test_db_name} already exists")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_test_database()
