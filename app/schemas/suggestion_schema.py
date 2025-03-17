from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class SuggestionBase(BaseModel):
    icon: str
    title: str
    description: str

class SuggestionCreate(SuggestionBase):
    user_id: str
    habit_data: Optional[Dict] = None  # Raw JSON data (optional)

class SuggestionResponse(SuggestionBase):
    id: str
    user_id: str
    habit_data: Optional[Dict]
    created_at: datetime
    is_viewed: bool = False
    is_implemented: bool = False

    class Config:
        from_attributes = True
