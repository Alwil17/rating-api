from sqlalchemy import Column, ForeignKey, Integer, Table
from app.domain.base import Base

item_tag = Table(
    "item_tag",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)