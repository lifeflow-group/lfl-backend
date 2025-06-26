from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from app.models.habit import RepeatFrequency


class HabitSeriesBase(BaseModel):
    """Basic schema used for HabitSeries"""

    user_id: str = Field(alias="userId")
    habit_id: str = Field(alias="habitId")
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="startDate"
    )
    until_date: Optional[datetime] = Field(default=None, alias="untilDate")
    repeat_frequency: RepeatFrequency = Field(
        default=RepeatFrequency.DAILY, alias="repeatFrequency"
    )

    class Config:
        populate_by_name = True
        from_attributes = True


class HabitSeriesResponse(HabitSeriesBase):
    """Schema for HabitSeries data response from API"""

    id: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="createdAt"
    )

    class Config:
        from_attributes = True
