from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone
from ..database import Base
from ..utils.id_generator import generate_uuid


class RepeatFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TrackingType(str, enum.Enum):
    COMPLETE = "complete"
    PROGRESS = "progress"


class Habit(Base):
    __tablename__ = "habits"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    category_id = Column(String, ForeignKey("categories.id"))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    habit_series_id = Column(String, nullable=True)
    reminder_enabled = Column(Boolean, default=False, nullable=False)
    tracking_type = Column(
        Enum(TrackingType), default=TrackingType.COMPLETE, nullable=False
    )
    target_value = Column(Integer, nullable=True)
    unit = Column(String, nullable=True)
    current_value = Column(Integer, nullable=True)
    is_completed = Column(Boolean, nullable=True)

    # Relationships
    user = relationship("User", back_populates="habits")
    category = relationship("Category", back_populates="habits")
    performance_metrics = relationship("PerformanceMetric", back_populates="habit")
    habit_series = relationship("HabitSeries", back_populates="habit", uselist=False)
    suggestions = relationship("Suggestion", back_populates="habit")
