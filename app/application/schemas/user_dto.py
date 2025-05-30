from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str
    role: Optional[str] = None
    image_url: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str]
    password: Optional[str] = None
    image_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
