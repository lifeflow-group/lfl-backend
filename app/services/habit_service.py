from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import uuid

from app.models.performance_metric import PerformanceMetric as PerformanceMetricModel
from app.schemas.habit_schema import HabitResponse as HabitSchema
from app.schemas.performance_metric_schema import PerformanceMetricResponse


# ==========================================================
# Calculate metrics (Rule-based logic)
# ==========================================================
def calculate_performance_metrics(
    habits: List[HabitSchema]
) -> List[PerformanceMetricResponse]:
    """
    Calculate performance metrics from Habit schemas.
    """

    metrics = []

    for habit in habits:
        start_date = habit.start_date or (datetime.now() - timedelta(days=30))
        end_date = datetime.now()

        # Fake history data for example (replace with real user data)
        history = _get_fake_history()

        completed_entries = sum(1 for entry in history if entry.get("completed", False))
        total_entries = len(history)

        completion_rate = (completed_entries / total_entries) * 100 if total_entries > 0 else 0
        average_progress = sum(entry.get("progress", 0) for entry in history) / len(history) if history else 0
        total_progress = habit.progress or 0

        description = generate_performance_description(habit.name, completion_rate)

        metric = PerformanceMetricResponse(
            id=str(uuid.uuid4()),
            user_id=habit.user_id,
            habit_id=habit.id,
            completion_rate=completion_rate,
            average_progress=average_progress,
            total_progress=total_progress,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_at=datetime.now()
        )

        metrics.append(metric)

    return metrics


# ==========================================================
# Utility functions
# ==========================================================
def generate_performance_description(habit_name: str, completion_rate: float) -> str:
    if completion_rate >= 80:
        return f"Excellent adherence to '{habit_name}' with {completion_rate:.1f}% completion rate."
    elif completion_rate >= 50:
        return f"Good progress on '{habit_name}' with {completion_rate:.1f}% completion rate."
    else:
        return f"Needs improvement on '{habit_name}' with only {completion_rate:.1f}% completion rate."


def _get_fake_history():
    """
    Fake history for testing; should be replaced with real habit tracking logs.
    """
    return [
        {"completed": True, "progress": 100},
        {"completed": False, "progress": 0},
        {"completed": True, "progress": 80},
        {"completed": True, "progress": 90},
    ]
