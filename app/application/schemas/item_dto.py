from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

from app.application.schemas.category_dto import CategoryDTO
from app.application.schemas.tag_dto import TagDTO

# ------------------------------
# Item DTOs et Réponses
# ------------------------------

class ItemBaseDTO(BaseModel):
    id: int
    name: str = Field(..., max_length=200)
    description: Optional[str]
    image_url: Optional[HttpUrl]
    categories: List[CategoryDTO] = []
    tags: list[TagDTO] = []
    created_at: datetime
    updated_at: datetime

class ItemCreateDTO(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_ids: Optional[List[int]] = []  # Existant
    tags: Optional[List[str]] = []   

class ItemUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

class ItemResponse(ItemBaseDTO):
    avg_rating: float = 0.0
    count_rating: int = 0

    model_config = ConfigDict(from_attributes=True, extra='allow')

