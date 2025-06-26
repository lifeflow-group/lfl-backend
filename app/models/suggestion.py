from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from ..utils.id_generator import generate_uuid
from datetime import datetime


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    habit_id = Column(String, ForeignKey("habits.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    user = relationship("User", back_populates="suggestions")
    habit = relationship("Habit", back_populates="suggestions")
    habit_plans = relationship(
        "HabitPlan", secondary="habit_plan_suggestions", back_populates="suggestions"
    )
