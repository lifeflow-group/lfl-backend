from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.habit_analysis_input_schema import HabitAnalysisInput
from app.schemas.habit_schema import HabitResponse
from app.schemas.performance_metric_schema import PerformanceMetricResponse
from app.services.habit_service import calculate_performance_metrics

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/metrics", response_model=List[PerformanceMetricResponse])
def analyze_habits_performance(habit_analysis_input: HabitAnalysisInput):
    """
    📊 Analyze Performance Metrics from Habits and save to DB
    """
    if not habit_analysis_input.habits:
        raise HTTPException(status_code=400, detail="No habits provided.")

    # Calculate Performance Metrics
    metrics = calculate_performance_metrics(habit_analysis_input)

    return metrics
