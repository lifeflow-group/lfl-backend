from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.habit import Habit as HabitModel
from app.schemas.habit_schema import HabitResponse
from app.schemas.performance_metric_schema import PerformanceMetricResponse
from app.schemas.suggestion_schema import SuggestionResponse
from app.models.suggestion import Suggestion as SuggestionModel
from app.services.ai_client import get_ai_suggestions
from app.utils.sample_suggestions import get_sample_suggestions


async def generate_suggestions(
    habits: List[HabitResponse],
    metrics: List[PerformanceMetricResponse]
) -> List[SuggestionResponse]:
    """
    Generate suggestions using AI based on habits and metrics.
    """
    ai_suggestions = await get_ai_suggestions(habits, metrics)

    user_id = habits[0].user_id if habits else None

    for suggestion in ai_suggestions:
        suggestion.user_id = user_id

    return ai_suggestions

def save_suggestions(
    db: Session,
    suggestions: List[SuggestionResponse]
) -> None:
    """
    Save generated suggestions to the database.
    For each suggestion:
    1. Create a new Habit from suggestion.habit_data.
    2. Save the Suggestion with the new habit_id.
    """
    for suggestion in suggestions:
        # Save the suggestion habit to the database
        habit_data = suggestion.habit_data
        
        suggestion_habit = HabitModel(
            # id=habit_data.get("id"),  # the id is auto-generated
            name=habit_data.get("name"),
            user_id=suggestion.user_id,
            category_id=habit_data.get("category_id"),
            start_date=habit_data.get("start_date"),
            repeat_frequency=habit_data.get("repeat_frequency"),
            reminder_enabled=habit_data.get("reminder_enabled", False),
            tracking_type=habit_data.get("tracking_type"),
            quantity=habit_data.get("quantity"),
            unit=habit_data.get("unit"),
            progress=habit_data.get("progress"),
            completed=habit_data.get("completed", False)
        )
        
        db.add(suggestion_habit)
        db.flush()
        
        # Save the suggestion to the database
        suggestions = SuggestionModel(
            # id=suggestion.id, # the id is auto-generated
            user_id=suggestion.user_id,
            habit_id=suggestion_habit.id,
            icon=suggestion.icon,
            title=suggestion.title,
            description=suggestion.description,
            created_at=suggestion.created_at
        )
        
        db.add(suggestions)
    
    db.commit()


async def generate_and_save_suggestions(
    db: Session,
    habits: List[HabitResponse],
    metrics: List[PerformanceMetricResponse]
) -> List[SuggestionResponse]:
    """
    Generate suggestions and save them to the database.
    """
    if not habits:
        raise ValueError("Habits list cannot be empty to determine user_id.")

    user_id = habits[0].user_id
    suggestions: List[SuggestionResponse] = []
    generate_ai = False

    try:
        # Step 1: Generate via AI
        suggestions = await generate_suggestions(habits, metrics)
        generate_ai = True
        print(f"Generated {len(suggestions)} suggestions via AI for user {user_id}")

    except Exception as e:
        print(f"AI suggestion generation failed: {str(e)}")

        # Step 2a: Fallback from DB (top 5, random order)
        suggestions = get_suggestion_by_user(db=db, user_id=user_id, limit=5, order_by='random')

        if suggestions:
            print(f"Fallback: Retrieved {len(suggestions)} suggestions from DB for user {user_id}")
        else:
            # Step 2b: Fallback to sample suggestions
            sample_data = get_sample_suggestions(user_id=user_id, limit=5)
            suggestions = [SuggestionResponse(**s) for s in sample_data]
            print(f"Fallback: Retrieved {len(suggestions)} sample suggestions for user {user_id}")

    # Step 3: Save suggestions to DB if AI-generated
    if generate_ai:
        save_suggestions(db, suggestions)
        print(f"Saved {len(suggestions)} AI suggestions to DB for user {user_id}")

    return suggestions

def get_suggestion_by_user(
    db: Session, 
    user_id: str, 
    limit: Optional[int] = None,  # Default is None -> fetch all
    order_by: str = "desc"        # "desc", "asc", or "random"
) -> List[SuggestionResponse]:
    
    # Validate order_by input
    order_by = order_by.lower()
    if order_by not in ["asc", "desc", "random"]:
        order_by = "desc"

    # Handle ordering logic
    if order_by == "random":
        ordering = func.random()
    elif order_by == "asc":
        ordering = SuggestionModel.created_at.asc()
    else:
        ordering = SuggestionModel.created_at.desc()

    # Query suggestions
    suggestions_query = (
        db.query(SuggestionModel)
        .filter(SuggestionModel.user_id == user_id)
        .order_by(ordering)
    )

    # If limit has a value other than None, apply the limit
    if limit is not None:
        suggestions_query = suggestions_query.limit(limit)

    suggestions = suggestions_query.all()

    # Habit mapping if there is a habit_id
    habit_ids = [s.habit_id for s in suggestions if s.habit_id]
    habits = db.query(HabitModel).filter(HabitModel.id.in_(habit_ids)).all()
    habit_map = {h.id: h for h in habits}

    def serialize_habit(habit: HabitModel):
        if not habit:
            return None
        return {
            "id": habit.id,
            "name": habit.name,
            "user_id": habit.user_id,
            "category_id": habit.category_id,
            "start_date": habit.start_date.isoformat() if habit.start_date else None,
            "repeat_frequency": getattr(habit.repeat_frequency, "value", None),
            "reminder_enabled": habit.reminder_enabled,
            "tracking_type": getattr(habit.tracking_type, "value", None),
            "quantity": habit.quantity,
            "unit": habit.unit,
            "progress": habit.progress,
            "completed": habit.completed
        }

    return [
        SuggestionResponse(
            id=s.id,
            user_id=s.user_id,
            icon=s.icon,
            title=s.title,
            description=s.description,
            created_at=s.created_at,
            habit_data=serialize_habit(habit_map.get(s.habit_id))
        )
        for s in suggestions
    ]
