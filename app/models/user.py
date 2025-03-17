from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base
from ..utils.id_generator import generate_uuid 

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, nullable=False)

    habits = relationship("Habit", back_populates="user")
    suggestions = relationship("Suggestion", back_populates="user")
