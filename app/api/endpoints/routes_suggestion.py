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

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])


@router.post("/analyze", response_model=List[SuggestionResponse])
async def analyze_and_suggest(
    habitAnalysisInput: HabitAnalysisInput, db: Session = Depends(get_db)
):
    """
    Analyze habits, automatically calculate performance metrics, generate suggestions and save everything to DB.

    **Input**:
    - habits: List of user habits

    **Output**:
    - suggestions: List of generated suggestions
    """

    if not habitAnalysisInput.habits:
        raise HTTPException(status_code=400, detail="No habits provided.")

    # 1. Calculate Performance Metrics from habits (Rule-Based or Pre-defined Logic)
    habitInputUpdate: HabitAnalysisInput = calculate_performance_metrics(
        habitAnalysisInput
    )

    # 2. Generate Suggestions based on habits and metrics
    # suggestions = await generate_and_save_suggestions(
    #     db=db, habitAnalysisInput=habitInputUpdate
    # )
    suggestions = await generate_suggestions(habitAnalysisInput=habitInputUpdate)

    print("Generated suggestions:", suggestions)

    return suggestions


@router.get("/", response_model=List[SuggestionResponse])
def get_suggestions(user_id: str = Query(...), db: Session = Depends(get_db)):
    """
    Get all suggestions for a specific user from the database.
    """
    suggestions = get_suggestion_by_user(db, user_id)
    return suggestions
