from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models.habit import RepeatFrequency
from app.utils.id_generator import generate_uuid


class HabitSeries(Base):
    __tablename__ = "habit_series"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    habit_id = Column(String, ForeignKey("habits.id"), nullable=False)
    start_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    until_date = Column(DateTime, nullable=True)
    repeat_frequency = Column(
        Enum(RepeatFrequency), nullable=False, default=RepeatFrequency.DAILY
    )

    # Relationship
    habit = relationship("Habit", back_populates="habit_series")
    habit_exceptions = relationship("HabitException", back_populates="habit_series")
