from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from typing import Optional
from datetime import datetime, date

class UserCreateDTO(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str
    role: Optional[str] = None
    image_url: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
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

# Admin Analytics DTOs
class UserGrowthDTO(BaseModel):
    date: date
    count: int

    class Config:
        orm_mode = True

class UserEngagementDTO(BaseModel):
    user_id: int
    username: str
    ratings_count: int
    last_activity: date

    class Config:
        orm_mode = True

class UserStatsDTO(BaseModel):
    total_users: int
    active_users: int
    new_users_today: int
    average_ratings_per_user: float

    class Config:
        orm_mode = True
