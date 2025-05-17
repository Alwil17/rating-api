# app/domain/models.py

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from app.domain.base import Base

class Rating(Base):
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)  # par exemple, note entre 0 et 5
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relations
    user = relationship("User", back_populates="ratings")
    item = relationship("Item", back_populates="ratings")
    
    def __repr__(self):
        return f"<Rating(id={self.id}, value={self.value}, user_id={self.user_id}, item_id={self.item_id})>"

