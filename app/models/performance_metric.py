from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.id_generator import generate_uuid
from ..database import Base

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    habit_id = Column(String, ForeignKey("habits.id"), index=True)
    completion_rate = Column(Float)
    average_progress = Column(Float)
    total_progress = Column(Float)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime)

    # Relationships
    habit = relationship("Habit", back_populates="performance_metrics")
