# app/application/schemas.py

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

# ------------------------------
# Rating DTOs et Réponses
# ------------------------------

class RatingCreateDTO(BaseModel):
    value: float = Field(..., ge=0, le=5)  # Note entre 0 et 5
    comment: Optional[str] = None
    user_id: int
    item_id: int

class RatingUpdateDTO(BaseModel):
    value: Optional[float] = Field(None, ge=0, le=5)
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    value: float
    comment: Optional[str]
    user_id: int
    item_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
