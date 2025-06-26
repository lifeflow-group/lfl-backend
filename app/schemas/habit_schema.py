from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.habit import TrackingType
from app.schemas.category_schema import CategoryResponse
from app.schemas.habit_series_schema import HabitSeriesResponse


class HabitBase(BaseModel):
    name: str
    tracking_type: TrackingType = Field(
        default=TrackingType.COMPLETE, alias="trackingType"
    )
    target_value: Optional[int] = Field(default=None, alias="targetValue")
    unit: Optional[str] = None
    reminder_enabled: bool = Field(default=False, alias="reminderEnabled")
    current_value: Optional[int] = Field(default=None, alias="currentValue")
    is_completed: Optional[bool] = Field(default=None, alias="isCompleted")
    date: datetime

    class Config:
        populate_by_name = True
        from_attributes = True


class HabitCreate(HabitBase):
    pass


class HabitResponse(HabitBase):
    id: str
    user_id: str = Field(alias="userId")
    category: CategoryResponse
    habit_series: Optional[HabitSeriesResponse] = Field(default=None, alias="series")

    class Config:
        populate_by_name = True
        from_attributes = True
