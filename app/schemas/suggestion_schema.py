from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict


class SuggestionBase(BaseModel):
    title: str
    description: str


class SuggestionCreate(SuggestionBase):
    user_id: str
    habit_data: Optional[Dict] = None  # Raw JSON data (optional)


class SuggestionResponse(SuggestionBase):
    id: str
    user_id: str = Field(None, alias="userId")
    habit_data: Optional[Dict] = Field(None, alias="habitData")
    created_at: datetime = Field(None, alias="createdAt")
    is_viewed: bool = Field(False, alias="isViewed")
    is_implemented: bool = Field(False, alias="isImplemented")

    class Config:
        populate_by_name = True
        from_attributes = True
