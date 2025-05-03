from sqlalchemy.orm import Session
from app.domain.category import Category

def seed_categories(db: Session):
    if db.query(Category).first():
        return  # Déjà seedé, on ne fait rien
    
    print("Seeding categories...")

    categories = [
        {"name": "Technology", "description": "Everything related to innovation and new technologies."},
        {"name": "Education", "description": "Category dedicated to educational resources and training."},
        {"name": "Home & Decor", "description": "Ideas and accessories to enhance your living space."},
        {"name": "Fashion & Accessories", "description": "Fashion trends and accessories for every style."},
        {"name": "Beauty & Health", "description": "Products for your well-being, beauty, and health."},
        {"name": "Food & Drinks", "description": "Everything about cooking, recipes, and healthy eating."},
        {"name": "Sports & Fitness", "description": "Gear and equipment for sports enthusiasts."},
        {"name": "Travel & Leisure", "description": "Destinations, activities, and leisure for travelers."},
        {"name": "Art & Music", "description": "Artistic inspiration and the world of music."},
        {"name": "Automotive", "description": "All about cars, motorcycles, and other vehicles."},
        {"name": "Books", "description": "Literary works ranging from classics to contemporary novels."},
        {"name": "Music", "description": "Albums, singles, and musical content across genres."},
        {"name": "Video Games", "description": "Interactive entertainment from indie to AAA titles."},
        {"name": "Movies", "description": "Films and cinema from classics to blockbusters."},
        {"name": "Photography", "description": "Cameras, techniques, and photographic art."},
    ]


    for category in categories:
        existing_category = db.query(Category).filter_by(name=category["name"]).first()
        if not existing_category:
            new_category = Category(name=category["name"], description=category["description"])
            db.add(new_category)
    
    db.commit()
    print("Catgories seeded!")
