from sqlalchemy.orm import Session
from app.domain.category import Category

def seed_categories(db: Session):
    if db.query(Category).first():
        return  # Déjà seedé, on ne fait rien
    
    categories = [
        {"name": "Technologie", "description": "Tout ce qui concerne l'innovation et les nouvelles technologies."},
        {"name": "Éducation", "description": "Catégorie dédiée aux ressources éducatives et à la formation."},
        {"name": "Maison & Décoration", "description": "Idées et accessoires pour améliorer votre intérieur."},
        {"name": "Mode & Accessoires", "description": "Tendances de mode et accessoires pour tous les styles."},
        {"name": "Beauté & Santé", "description": "Produits pour votre bien-être, beauté et santé."},
        {"name": "Alimentation", "description": "Tout sur la cuisine, les recettes et l'alimentation saine."},
        {"name": "Sport & Fitness", "description": "Articles et équipements pour les passionnés de sport."},
        {"name": "Voyages & Loisirs", "description": "Destinations, activités et loisirs pour les voyageurs."},
        {"name": "Art & Musique", "description": "Inspiration artistique et monde de la musique."},
        {"name": "Automobile", "description": "Tout sur les voitures, motos et autres véhicules."},
    ]

    for category in categories:
        existing_category = db.query(Category).filter_by(name=category["name"]).first()
        if not existing_category:
            new_category = Category(name=category["name"], description=category["description"])
            db.add(new_category)
    
    db.commit()
    print(f"{len(categories)} catégories ajoutées (ou déjà existantes).")
