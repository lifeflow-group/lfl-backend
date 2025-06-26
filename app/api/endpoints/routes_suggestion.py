from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.habit_analysis_input_schema import HabitAnalysisInput
from app.schemas.suggestion_schema import SuggestionResponse

from app.services.habit_service import calculate_performance_metrics
from app.services.suggestion_service import (
    generate_and_save_suggestions,
    generate_suggestions,
    get_suggestion_by_user,
)
from app.dependencies import get_db
from app.models.user import User  # Import the User model

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])


@router.post("/analyze", response_model=List[SuggestionResponse])
async def analyze_and_suggest(
    habitAnalysisInput: HabitAnalysisInput, db: Session = Depends(get_db)
):
    """
    Analyze habits, automatically calculate performance metrics, generate suggestions and save everything to DB.
    If the user_id does not exist, a new user will be created.

    **Input**:
    - userId: ID of the user
    - habits: List of user habits

    **Output**:
    - suggestions: List of generated suggestions
    """

    print("Received habit analysis input:", habitAnalysisInput)

    # Check if the user exists, if not, create one
    user = db.query(User).filter(User.id == habitAnalysisInput.user_id).first()
    if not user:
        print(
            f"User with id '{habitAnalysisInput.user_id}' not found. Creating new user."
        )
        new_user = User(
            id=habitAnalysisInput.user_id,
            name=f"User {habitAnalysisInput.user_id}",  # Or some default name
            # Add other default fields for User if necessary
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Created new user: {new_user.id}")
    else:
        print(f"User {user.id} found.")

    # 1. Calculate Performance Metrics from habits (Rule-Based or Pre-defined Logic)
    habitInputUpdate: HabitAnalysisInput = calculate_performance_metrics(
        habitAnalysisInput
    )

    # 2. Generate Suggestions based on habits and metrics
    suggestions = await generate_and_save_suggestions(
        db=db, habitAnalysisInput=habitInputUpdate
    )
    # suggestions = await generate_suggestions(habitAnalysisInput=habitInputUpdate)

    print("Generated suggestions:", suggestions)

    return suggestions


@router.get("/", response_model=List[SuggestionResponse])
def get_suggestions(user_id: str = Query(...), db: Session = Depends(get_db)):
    """
    Get all suggestions for a specific user from the database.
    """
    suggestions = get_suggestion_by_user(db, user_id)
    return suggestions
