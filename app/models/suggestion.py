from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.id_generator import generate_uuid
from ..database import Base


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    habit_id = Column(String, ForeignKey("habits.id"), index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="suggestions")
    habit = relationship("Habit", back_populates="suggestions")
