# Rating API - Comprehensive Rating & Review Platform

Rating API is a full-featured rating and review platform built with a modern tech stack. It allows users to rate and review items, discover new content through recommendations, and provides administrators with powerful analytics tools.

## 🚀 Features

### User Features
- **User Authentication** - Secure login/signup system
- **Item Rating & Reviews** - Rate items on a 1-5 scale and leave detailed comments
- **Personal Recommendations** - Get personalized recommendations based on rating history
- **Profile Management** - Update personal information and view rating history

### Admin Features
- **Complete User Management** - Create, update, and manage user accounts
- **Item Management** - Add, update, and categorize items
- **Category System** - Organize items into customizable categories
- **Tag System** - Add flexible tags to better describe items
- **Content Moderation** - Remove inappropriate reviews/comments
- **Analytics Dashboard** - Comprehensive analytics including:
  - Rating distributions
  - User growth metrics
  - Engagement statistics
  - Overall platform performance

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance API framework
- **SQLAlchemy** - ORM for database interactions
- **PostgreSQL** - Robust relational database
- **Pydantic** - Data validation and settings management
- **JWT** - Token-based authentication

### Frontend
- **Next.js** - React framework for web interface
- **React Query** - Data fetching and state management
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization

## 📋 Project Structure

```
RatingApp/
│
├── app/                          # Backend application
│   ├── api/                      # API routes and endpoints
│   │   ├── endpoints/            # Individual route modules
│   │   ├── auth.py               # Authentication handlers
│   │   └── security.py           # Security utilities
│   │
│   ├── application/              # Application layer
│   │   ├── schemas/              # Pydantic schemas/DTOs
│   │   └── services/             # Business logic services
│   │
│   ├── domain/                   # Domain models
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   └── rating.py
│   │
│   ├── infrastructure/           # Data access layer
│   │   ├── repositories/         # Repository pattern implementations
│   │   └── database.py           # Database connection
│   │
│   ├── config.py                 # Application configuration
│   └── main.py                   # Application entry point
│
├── migrations/                   # Database migration files
├── tests/                        # Test suite
├── docker/                       # Docker configuration
│   ├── Dockerfile.api            # API service Dockerfile
│   ├── Dockerfile.frontend       # Frontend Dockerfile
│   └── docker-compose.yml        # Docker composition
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
└── README.md                     # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Alwil17/rating-api.git
cd rating-api
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

5. Initialize the database migrations:
```bash
# Make sure your database connection details are in .env file
# DATABASE_URL=postgresql://username:password@localhost:5432/ratingapp

# Create the versions directory if it doesn't exist
mkdir -p alembic/versions

# Create a new migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migrations
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn app.api.main:app --reload
```

## 🐳 Docker Setup

For a quick setup with Docker:

```bash
docker-compose up -d
```

This will start both the backend API and frontend services, along with a PostgreSQL database.

## 🔒 API Authentication

The API uses JWT tokens for authentication:

1. Get a token by calling POST `/auth/token` with email and password
2. Include the token in subsequent requests as a Bearer token in the Authorization header

## 🧪 Testing

### Setting up a test database

Before running tests, you need to set up a test database:

```bash
# Create the test database
python setup_test_db.py
```

### Running tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

Tests use a separate database named `rating_db_test` by default to avoid affecting your development or production data.

## 📚 API Documentation

API documentation is automatically generated and available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.