from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HabitExceptionBase(BaseModel):
    """Basic schema for HabitException"""

    habit_series_id: str = Field(..., alias="habitSeriesId")
    date: datetime = Field(..., alias="date")
    is_skipped: bool = Field(False, alias="isSkipped")
    reminder_enabled: bool = Field(False, alias="reminderEnabled")
    target_value: Optional[int] = Field(None, alias="targetValue")
    current_value: Optional[int] = Field(None, alias="currentValue")
    is_completed: Optional[bool] = Field(None, alias="isCompleted")

    class Config:
        populate_by_name = True
        from_attributes = True


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
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True
        from_attributes = True
