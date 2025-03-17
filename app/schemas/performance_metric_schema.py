from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PerformanceMetricBase(BaseModel):
    completion_rate: float
    average_progress: float
    total_progress: float
    description: Optional[str]
    start_date: datetime
    end_date: datetime

class PerformanceMetricCreate(PerformanceMetricBase):
    habit_id: Optional[str]

class PerformanceMetricResponse(PerformanceMetricBase):
    id: str
    habit_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
