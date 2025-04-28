from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from app.domain.item_category import item_category
from app.domain.item_tag import item_tag
from app.domain.base import Base

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation vers les categories
    categories = relationship("Category",back_populates="items", secondary=item_category)
    # Relation vers les tags
    tags = relationship("Tag", back_populates="items", secondary=item_tag)
    # Relation vers les ratings
    ratings = relationship("Rating", back_populates="item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}')>"
