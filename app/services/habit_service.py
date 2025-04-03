import calendar
from typing import List
from datetime import datetime, timedelta
import uuid

from app.models.habit import RepeatFrequency, TrackingType
from app.models.performance_metric import PerformanceMetric
from app.schemas.habit_analysis_input_schema import HabitAnalysisInput, HabitData
from app.schemas.habit_exception_schema import HabitExceptionBase
from app.schemas.performance_metric_schema import PerformanceMetricResponse


def calculate_performance_metrics(
    habit_analysis_input: HabitAnalysisInput,
) -> HabitAnalysisInput:
    """
    Calculate performance metrics for each habit based on generated Habit Instances.
    """

    updated_habits = []

    for habit in habit_analysis_input.habits:
        # Generate Habit Instances
        habit_instances = generate_habit_instances(habit, habit_analysis_input.end_date)

        # Apply exceptions
        habit_instances = apply_exceptions(habit_instances, habit.exceptions)

        # Calculate performance metrics
        performance_metric = compute_performance_metric(habit, habit_instances)

        # Update HabitData with performance_metric
        updated_habit = habit.model_copy(
            update={"performance_metric": performance_metric}
        )
        updated_habits.append(updated_habit)

    # Return updated HabitAnalysisInput with modified habits
    return habit_analysis_input.model_copy(update={"habits": updated_habits})


# ==========================================================
# Helper Functions
# ==========================================================


def generate_habit_instances(habit: HabitData, end_date: datetime) -> List[dict]:
    """
    Generate Habit Instances based on repeat_frequency, ensuring that dates do not exceed `end_date`.
    """
    instances = []
    current_date = habit.start_date

    # Determine the actual end date (take the minimum date between until_date and end_date)
    final_date = min(habit.until_date, end_date) if habit.until_date else end_date

    while current_date <= final_date:
        instances.append(
            {
                "date": current_date,
                "is_completed": False,  # Default: not completed
                "current_value": 0,  # Default current_value = 0
            }
        )

        # Move to next occurrence based on repeat_frequency
        if habit.repeat_frequency == RepeatFrequency.DAILY:
            current_date += timedelta(days=1)
        elif habit.repeat_frequency == RepeatFrequency.WEEKLY:
            current_date += timedelta(weeks=1)
        elif habit.repeat_frequency == RepeatFrequency.MONTHLY:
            current_date = add_months(current_date, 1)
        else:
            break  # Stop if frequency is not set

    return instances


def apply_exceptions(
    instances: List[dict], exceptions: List[HabitExceptionBase]
) -> List[dict]:
    """
    Apply habit exceptions (skip days, modify progress) to instances.
    """
    for exception in exceptions:
        for instance in instances:
            if instance["date"].date() == exception.date.date():
                if exception.is_skipped:
                    instances.remove(instance)  # Skip this instance
                else:
                    # Update instance based on exception values
                    instance["is_completed"] = (
                        exception.is_completed
                        if exception.is_completed is not None
                        else instance["is_completed"]
                    )
                    instance["current_value"] = (
                        exception.target_value
                        if exception.target_value is not None
                        else instance["current_value"]
                    )

    return instances


def compute_performance_metric(
    habit: HabitData, instances: List[dict]
) -> PerformanceMetric:
    """
    Compute performance metrics based on completed instances and progress tracking.
    """
    total_instances = len(instances)
    completed_instances = sum(1 for i in instances if i["is_completed"])
    total_progress = sum(i["current_value"] for i in instances)

    if habit.tracking_type == TrackingType.COMPLETE:
        completion_rate = (
            (completed_instances / total_instances) * 100 if total_instances > 0 else 0
        )
        score = completion_rate  # Score = completion rate (0-100)
        average_progress = None
    else:
        completion_rate = None
        average_progress = (
            total_progress / total_instances if total_instances > 0 else 0
        )
        score = (
            (total_progress / (habit.target_value * total_instances)) * 100
            if habit.target_value
            else 0
        )

    description = generate_performance_description(habit.name, score)

    return PerformanceMetricResponse(
        id=str(uuid.uuid4()),
        habit_id=habit.id,
        score=score,
        completion_rate=completion_rate,
        average_progress=average_progress,
        total_progress=total_progress,
        description=description,
        created_at=datetime.now(),
    )


def generate_performance_description(habit_name: str, score: float) -> str:
    """
    Generate a descriptive performance message based on the score.
    """
    if score >= 85:
        return f"Outstanding consistency with '{habit_name}', achieving {score:.1f}%!"
    elif score >= 70:
        return f"Great progress on '{habit_name}', with a strong {score:.1f}% success rate."
    elif score >= 55:
        return f"Steady effort in '{habit_name}', but there's room for improvement ({score:.1f}%)."
    elif score >= 40:
        return f"Needs more consistency in '{habit_name}', only reaching {score:.1f}%."
    elif score >= 25:
        return f"Limited engagement with '{habit_name}', achieving just {score:.1f}%."
    else:
        return f"Minimal progress in '{habit_name}', with only {score:.1f}% success."


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return source_date.replace(year=year, month=month, day=day)
