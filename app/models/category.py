from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base
from ..utils.id_generator import generate_uuid


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=True)
    color_hex = Column(String, nullable=True)

    # Relationships
    habits = relationship("Habit", back_populates="category")
    habit_plans = relationship("HabitPlan", back_populates="category")
