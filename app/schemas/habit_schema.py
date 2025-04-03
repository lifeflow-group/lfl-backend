from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.habit import RepeatFrequency, TrackingType
from app.schemas.habit_category_schema import HabitCategoryResponse


class HabitBase(BaseModel):
    name: str
    category_id: str
    habit_series_id: Optional[str]
    tracking_type: TrackingType = TrackingType.COMPLETE
    target_value: Optional[int]
    unit: Optional[str]
    reminder_enabled: bool = False


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str]
    category_id: Optional[str]
    habit_series_id: Optional[str]
    tracking_type: Optional[TrackingType]
    target_value: Optional[int]
    unit: Optional[str]
    reminder_enabled: Optional[bool]


class HabitResponse(HabitBase):
    id: str
    user_id: str
    category: HabitCategoryResponse
    current_value: Optional[int]
    is_completed: Optional[bool]
    start_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
