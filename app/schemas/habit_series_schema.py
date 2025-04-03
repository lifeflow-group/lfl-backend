from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from app.models.habit import RepeatFrequency


class HabitSeriesBase(BaseModel):
    """Basic schema used for HabitSeries"""
    habit_id: str
    start_date: datetime = datetime.now(timezone.utc)
    until_date: Optional[datetime] = None
    repeat_frequency: RepeatFrequency = RepeatFrequency.DAILY


class HabitSeriesCreate(HabitSeriesBase):
    """Schema used when creating a new HabitSeries"""
    pass


class HabitSeriesUpdate(BaseModel):
    """Schema used when updating a HabitSeries"""
    start_date: Optional[datetime]
    until_date: Optional[datetime]
    repeat_frequency: Optional[RepeatFrequency]


class HabitSeriesResponse(HabitSeriesBase):
    """Schema for HabitSeries data response from API"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
