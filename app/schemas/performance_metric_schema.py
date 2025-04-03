from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PerformanceMetricBase(BaseModel):
    score: float
    completion_rate: Optional[float]
    average_progress: Optional[float]
    total_progress: Optional[float]
    description: Optional[str]


class PerformanceMetricCreate(PerformanceMetricBase):
    habit_id: Optional[str]


class PerformanceMetricResponse(PerformanceMetricBase):
    id: str
    habit_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
