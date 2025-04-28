from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.domain.base import Base
from .item_category import item_category

class Category(Base):
    __tablename__ = "categories"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=True)

    # back-ref vers items
    items = relationship(
        "Item",
        secondary=item_category,
        back_populates="categories"
    )
