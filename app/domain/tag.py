# app/domain/models/tag.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.domain.base import Base
from .item_tag import item_tag

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    items = relationship("Item", secondary=item_tag, back_populates="tags")
