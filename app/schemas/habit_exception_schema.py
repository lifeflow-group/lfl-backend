from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitExceptionBase(BaseModel):
    """Basic schema for HabitException"""
    habit_series_id: str
    date: datetime
    is_skipped: bool = False
    reminder_enabled: bool = False
    target_value: Optional[int] = None
    current_value: Optional[int] = None
    is_completed: Optional[bool] = None


class HabitExceptionCreate(HabitExceptionBase):
    """Schema used when creating a new HabitException"""
    pass


class HabitExceptionUpdate(BaseModel):
    """Schema used when updating a HabitException"""
    date: Optional[datetime]
    is_skipped: Optional[bool]
    reminder_enabled: Optional[bool]
    target_value: Optional[int]
    current_value: Optional[int]
    is_completed: Optional[bool]


class HabitExceptionResponse(HabitExceptionBase):
    """Schema for HabitException data response from API"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
