from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.schemas.habit_schema import HabitResponse


class SuggestionBase(BaseModel):
    title: str
    description: str


class SuggestionCreate(SuggestionBase):
    user_id: str
    habit: Optional[HabitResponse] = None  # Raw JSON data (optional)


class SuggestionResponse(SuggestionBase):
    id: str
    user_id: str = Field(None, alias="userId")
    habit: Optional[HabitResponse] = None
    created_at: datetime = Field(None, alias="createdAt")

    class Config:
        populate_by_name = True
        from_attributes = True
