from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.habit_plan import HabitPlan
from app.models.suggestion import Suggestion
from app.schemas.habit_plan_schema import HabitPlanResponse


def get_habit_plans(
    db: Session, skip: int = 0, limit: int = 100
) -> List[HabitPlanResponse]:
    """Get all habit plans and convert to response schema"""
    db_plans = (
        db.query(HabitPlan)
        .options(joinedload(HabitPlan.category))
        .options(joinedload(HabitPlan.suggestions).joinedload(Suggestion.habit))
        .offset(skip)
        .limit(limit)
        .all()
    )
    # Convert model to dict before validation to handle nested relationships
    results = []
    for plan in db_plans:
        try:
            results.append(HabitPlanResponse.model_validate(plan))
        except Exception as e:
            print(f"Error validating plan {plan.id}: {e}")
    return results


def get_habit_plan_by_id(db: Session, plan_id: str) -> Optional[HabitPlanResponse]:
    """Get a specific habit plan by ID and convert to response schema"""
    db_plan = (
        db.query(HabitPlan)
        .options(joinedload(HabitPlan.category))
        .options(joinedload(HabitPlan.suggestions).joinedload(Suggestion.habit))
        .filter(HabitPlan.id == plan_id)
        .first()
    )
    if db_plan:
        try:
            return HabitPlanResponse.model_validate(db_plan)
        except Exception as e:
            print(f"Error validating plan {plan_id}: {e}")
            return None
    return None


def get_habit_plans_by_category(
    db: Session, category_id: str
) -> List[HabitPlanResponse]:
    """Get all habit plans for a specific category and convert to response schema"""
    db_plans = (
        db.query(HabitPlan)
        .options(joinedload(HabitPlan.category))
        .options(joinedload(HabitPlan.suggestions).joinedload(Suggestion.habit))
        .filter(HabitPlan.category_id == category_id)
        .all()
    )
    results = []
    for plan in db_plans:
        try:
            results.append(HabitPlanResponse.model_validate(plan))
        except Exception as e:
            print(f"Error validating plan {plan.id}: {e}")
    return results
