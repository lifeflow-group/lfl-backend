from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.utils.id_generator import generate_uuid


class HabitException(Base):
    __tablename__ = "habit_exceptions"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    habit_series_id = Column(
        String, ForeignKey("habit_series.id"), nullable=False
    )  # Link to HabitSeries
    date = Column(DateTime, nullable=False)  # Exception application date
    is_skipped = Column(
        Boolean, default=False, nullable=False
    )  # If true, skip this date
    reminder_enabled = Column(Boolean, default=False, nullable=False)
    target_value = Column(Integer, nullable=True)
    current_value = Column(Integer, nullable=True)
    is_completed = Column(Boolean, nullable=True)

    # Relationships
    habit_series = relationship("HabitSeries", back_populates="habit_exceptions")
