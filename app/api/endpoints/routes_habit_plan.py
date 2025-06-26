from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.habit_plan_schema import HabitPlanResponse
from app.services.habit_plan_service import (
    get_habit_plans,
    get_habit_plan_by_id,
    get_habit_plans_by_category,
)
from app.dependencies import get_db

router = APIRouter(prefix="/habit-plans", tags=["Habit Plans"])


@router.get("/", response_model=List[HabitPlanResponse])
def read_habit_plans(
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
):
    """
    Get all habit plans, with optional filtering by category.
    """
    if category_id:
        return get_habit_plans_by_category(db, category_id)
    return get_habit_plans(db, skip=skip, limit=limit)


@router.get("/{plan_id}", response_model=HabitPlanResponse)
def read_habit_plan(plan_id: str, db: Session = Depends(get_db)):
    """
    Get a specific habit plan by ID.
    """
    db_plan = get_habit_plan_by_id(db, plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Habit plan not found")
    return db_plan
