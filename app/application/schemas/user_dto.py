from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str

class UserUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Optionnel en cas de changement de mot de passe

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
