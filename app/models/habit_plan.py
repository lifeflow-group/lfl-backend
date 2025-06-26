from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.id_generator import generate_uuid
from ..database import Base


class HabitPlan(Base):
    __tablename__ = "habit_plans"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    image_path = Column(String, nullable=True)

    # Relationships
    category = relationship("Category", back_populates="habit_plans")
    suggestions = relationship(
        "Suggestion", secondary="habit_plan_suggestions", back_populates="habit_plans"
    )


class HabitPlanSuggestion(Base):
    __tablename__ = "habit_plan_suggestions"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    habit_plan_id = Column(
        String, ForeignKey("habit_plans.id"), nullable=False, index=True
    )
    suggestion_id = Column(
        String, ForeignKey("suggestions.id"), nullable=False, index=True
    )
