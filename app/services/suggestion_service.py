from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.habit import Habit as HabitModel
from app.models.category import Category
from app.models.habit_series import HabitSeries as HabitSeriesModel
from app.schemas.habit_analysis_input_schema import HabitAnalysisInput
from app.schemas.suggestion_schema import SuggestionResponse
from app.models.suggestion import Suggestion as SuggestionModel
from app.services.ai_client import get_ai_suggestions
from app.utils.sample_suggestions import get_sample_suggestions


async def generate_suggestions(
    habitAnalysisInput: HabitAnalysisInput,
) -> List[SuggestionResponse]:
    """
    Generate suggestions using AI based on habits and metrics.
    """
    ai_suggestions = await get_ai_suggestions(habitAnalysisInput)

    user_id = habitAnalysisInput.user_id

    for suggestion in ai_suggestions:
        suggestion.user_id = user_id

    return ai_suggestions


def save_suggestions(
    db: Session, suggestions: List[SuggestionResponse], user_id: str
) -> None:
    """
    Save generated suggestions to the database.
    For each suggestion:
    1. Create a new Habit from suggestion.habit.
    2. Create a new HabitSeries and link it to the Habit.
    3. Save the Suggestion with the new habit_id.
    """
    for suggestion in suggestions:
        # Extract habit data from suggestion and convert to dict
        habit_data = suggestion.habit
        if not habit_data:
            continue  # Skip if no habit data

        # Convert Pydantic model to dict
        habit_dict = habit_data.model_dump()

        # Now you can use .get() method
        series_data = habit_dict.get("series")

        # 1. Create HabitModel first
        suggestion_habit = HabitModel(
            name=habit_dict.get("name"),
            user_id=user_id,
            category_id=(
                habit_dict.get("category", {}).get("id")
                if habit_dict.get("category")
                else None
            ),
            date=habit_dict.get("date"),
            reminder_enabled=habit_dict.get("reminderEnabled", False),
            tracking_type=habit_dict.get("trackingType"),
            target_value=habit_dict.get("targetValue"),
            current_value=habit_dict.get("currentValue", 0),
            is_completed=habit_dict.get("isCompleted", False),
            unit=habit_dict.get("unit"),
        )

        db.add(suggestion_habit)
        db.flush()  # Get the generated ID

        # 2. Create HabitSeries and link it to HabitModel (if series data exists)
        if series_data:
            habit_series = HabitSeriesModel(
                user_id=user_id,
                habit_id=suggestion_habit.id,
                start_date=series_data.get("startDate"),
                until_date=series_data.get("untilDate"),
                repeat_frequency=series_data.get("repeatFrequency"),
            )
            db.add(habit_series)
            db.flush()  # Get the generated ID

            # Update habit with habit_series_id reference
            suggestion_habit.habit_series_id = habit_series.id
            db.flush()

        # 3. Save the suggestion to the database
        db_suggestion = SuggestionModel(
            user_id=user_id,
            habit_id=suggestion_habit.id,
            title=suggestion.title,
            description=suggestion.description,
            created_at=suggestion.created_at,
        )

        db.add(db_suggestion)

    # Commit all changes at once
    db.commit()


async def generate_and_save_suggestions(
    db: Session,
    habitAnalysisInput: HabitAnalysisInput,
) -> List[SuggestionResponse]:
    """
    Generate suggestions and save them to the database.
    """

    user_id = habitAnalysisInput.user_id
    suggestions: List[SuggestionResponse] = []
    generate_ai = False

    try:
        # Step 1: Generate via AI
        suggestions = await generate_suggestions(habitAnalysisInput)
        generate_ai = True
        print(f"Generated {len(suggestions)} suggestions via AI for user {user_id}")

    except Exception as e:
        print(f"AI suggestion generation failed: {str(e)}")

        # Step 2a: Fallback from DB (top 5, random order)
        suggestions = get_suggestion_by_user(
            db=db, user_id=user_id, limit=5, order_by="random"
        )

        if suggestions:
            print(
                f"Fallback: Retrieved {len(suggestions)} suggestions from DB for user {user_id}"
            )
        else:
            # Step 2b: Fallback to sample suggestions
            sample_data = get_sample_suggestions(user_id=user_id, limit=5)
            suggestions = [SuggestionResponse(**s) for s in sample_data]
            print(
                f"Fallback: Retrieved {len(suggestions)} sample suggestions for user {user_id}"
            )

    # Step 3: Save suggestions to DB if AI-generated
    if generate_ai:
        # TODO: save_suggestions after have updated suggestion
        save_suggestions(db, suggestions, user_id)
        print(f"Saved {len(suggestions)} AI suggestions to DB for user {user_id}")

    return suggestions


def get_suggestion_by_user(
    db: Session,
    user_id: str,
    limit: Optional[int] = None,  # Default is None -> fetch all
    order_by: str = "desc",  # "desc", "asc", or "random"
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

        # Fetch category
        category = db.query(Category).filter(Category.id == habit.category_id).first()

        # Fetch HabitSeries
        habit_series = (
            db.query(HabitSeriesModel)
            .filter(HabitSeriesModel.id == habit.habit_series_id)
            .first()
        )

        return {
            "id": habit.id,
            "name": habit.name,
            "userId": user_id,  # Thêm userId từ tham số hoặc từ habit
            "category": (
                {
                    "id": category.id if category else None,
                    "name": (
                        category.name if category else None
                    ),  # Đổi từ label sang name
                    "iconPath": category.icon_path if category else None,
                    "colorHex": (
                        category.color_hex if category else "#000000"
                    ),  # Thêm colorHex
                }
                if category
                else None
            ),
            "date": habit.date.isoformat() if habit.date else None,
            "series": (
                {
                    "id": habit_series.id if habit_series else None,
                    "userId": user_id,
                    "habitId": habit.id,
                    "startDate": (
                        habit_series.start_date.isoformat() if habit_series else None
                    ),
                    "untilDate": (
                        habit_series.until_date.isoformat()
                        if habit_series and habit_series.until_date
                        else None
                    ),
                    "repeatFrequency": (
                        habit_series.repeat_frequency if habit_series else None
                    ),
                }
                if habit_series
                else None
            ),
            "reminderEnabled": habit.reminder_enabled,
            "trackingType": getattr(habit.tracking_type, "value", None),
            "targetValue": habit.target_value,
            "currentValue": (
                habit.current_value if hasattr(habit, "current_value") else 0
            ),
            "unit": habit.unit,
            "isCompleted": (
                habit.is_completed if hasattr(habit, "is_completed") else False
            ),
        }

    return [
        SuggestionResponse(
            id=s.id,
            user_id=s.user_id,
            title=s.title,
            description=s.description,
            created_at=s.created_at,
            habit=serialize_habit(habit_map.get(s.habit_id)),
        )
        for s in suggestions
    ]
