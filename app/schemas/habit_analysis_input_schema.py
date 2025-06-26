from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.category_schema import CategoryResponse
from app.schemas.habit_exception_schema import HabitExceptionResponse
from app.models.habit import RepeatFrequency, TrackingType
from app.schemas.performance_metric_schema import PerformanceMetricResponse


class HabitData(BaseModel):
    """Data for each habit in the analysis"""

    id: str = Field(..., alias="id")  # Can use alias here if needed
    name: str = Field(..., alias="name")
    category: CategoryResponse = Field(..., alias="category")
    tracking_type: TrackingType = Field(
        ..., alias="trackingType"
    )  # Example camelCase alias

    # TrackingType = progress
    target_value: Optional[int] = Field(None, alias="targetValue")  # camelCase alias
    unit: Optional[str] = Field(None, alias="unit")

    # Recurrence Rule
    repeat_frequency: Optional[RepeatFrequency] = Field(
        None, alias="repeatFrequency"
    )  # camelCase alias
    start_date: datetime = Field(..., alias="startDate")  # camelCase alias
    until_date: Optional[datetime] = Field(None, alias="untilDate")  # camelCase alias

    # List of exceptions
    exceptions: List[HabitExceptionResponse] = Field([], alias="exceptions")

    performance_metric: Optional[PerformanceMetricResponse] = Field(
        None, alias="performanceMetric"
    )

    class Config:
        # Allow using aliases and keep the original field names in Python
        populate_by_name = True
        from_attributes = True


class HabitAnalysisInput(BaseModel):
    """Input data for habit analysis"""

    user_id: str = Field(..., alias="userId")  # camelCase alias
    start_date: datetime = Field(..., alias="startDate")  # camelCase alias
    end_date: datetime = Field(..., alias="endDate")  # camelCase alias
    habits: List[HabitData] = Field([], alias="habits")

    class Config:
        populate_by_name = True  # Allow using original field names
        from_attributes = True
