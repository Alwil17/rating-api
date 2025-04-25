from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from typing import Optional
from datetime import datetime

# ------------------------------
# Item DTOs et Réponses
# ------------------------------

class ItemBaseDTO(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str]

class ItemCreateDTO(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None

class ItemUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

class ItemResponse(ItemBaseDTO):
    id: int
    image_url: Optional[HttpUrl]  # URL validée
    avg_rating: float
    count_rating: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

