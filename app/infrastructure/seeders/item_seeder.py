from sqlalchemy.orm import Session
from app.domain.item import Item
from app.domain.category import Category

# Exemple simple de seed pour les items
def seed_items(db: Session):
    if db.query(Item).first():
        return  # Déjà seedé, on ne fait rien
    
    print("Seeding items...")
    
    # Liste des items avec leur(s) catégorie(s)
    items_data = [
        {"name": "The Great Gatsby", "description": "A classic novel by F. Scott Fitzgerald.", "category_names": ["Books"]},
        {"name": "1984", "description": "A dystopian novel by George Orwell.", "category_names": ["Books"]},
        {"name": "Thriller - Michael Jackson", "description": "The best-selling album of all time.", "category_names": ["Music"]},
        {"name": "Bohemian Rhapsody - Queen", "description": "A legendary rock song blending genres.", "category_names": ["Music"]},
        {"name": "The Legend of Zelda: Breath of the Wild", "description": "An open-world adventure game by Nintendo.", "category_names": ["Video Games"]},
        {"name": "The Witcher 3: Wild Hunt", "description": "An award-winning fantasy RPG.", "category_names": ["Video Games"]},
        {"name": "Inception", "description": "A sci-fi thriller by Christopher Nolan.", "category_names": ["Movies"]},
        {"name": "The Godfather", "description": "A classic crime film directed by Francis Ford Coppola.", "category_names": ["Movies"]},
        {"name": "iPhone 14 Pro", "description": "Apple's flagship smartphone with advanced cameras.", "category_names": ["Technology"]},
        {"name": "MacBook Air M2", "description": "Lightweight and powerful laptop for professionals.", "category_names": ["Technology"]},
        {"name": "Mona Lisa", "description": "The world’s most famous portrait by Leonardo da Vinci.", "category_names": ["Art"]},
        {"name": "The Starry Night", "description": "Iconic painting by Vincent van Gogh.", "category_names": ["Art"]},
        {"name": "Cheeseburger", "description": "A juicy grilled beef burger with cheese.", "category_names": ["Food"]},
        {"name": "Sushi", "description": "Traditional Japanese dish with vinegared rice and seafood.", "category_names": ["Food"]},
        {"name": "Canon EOS R5", "description": "A high-end mirrorless camera for professionals.", "category_names": ["Photography"]},
        {"name": "Nikon Z6 II", "description": "A versatile full-frame camera for creators.", "category_names": ["Photography"]},
    ]

    for item_info in items_data:
        # Vérifier si l'item existe déjà pour éviter les doublons
        existing_item = db.query(Item).filter_by(name=item_info["name"]).first()
        if existing_item:
            continue

        # Créer l'item
        item = Item(
            name=item_info["name"],
            description=item_info["description"],
        )

        # Associer les catégories
        for cat_name in item_info["category_names"]:
            category = db.query(Category).filter_by(name=cat_name).first()
            if category:
                item.categories.append(category)

        db.add(item)

    db.commit()
    print("Items seeded!")
