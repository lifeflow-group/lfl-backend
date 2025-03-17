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
    category_id = Column(String, ForeignKey("habit_categories.id"))
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    repeat_frequency = Column(Enum(RepeatFrequency), nullable=True)
    reminder_enabled = Column(Boolean, default=False, nullable=False)
    tracking_type = Column(Enum(TrackingType), default=TrackingType.COMPLETE, nullable=False)
    quantity = Column(Integer, nullable=True)
    unit = Column(String, nullable=True)
    progress = Column(Integer, nullable=True)
    completed = Column(Boolean, nullable=True)

    # relationships
    user = relationship("User", back_populates="habits")
    category = relationship("HabitCategory")
    performance_metrics = relationship("PerformanceMetric", back_populates="habit")
    suggestions = relationship("Suggestion", back_populates="habit")
