from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.category_schema import CategoryResponse
from app.schemas.suggestion_schema import SuggestionResponse


class HabitPlanBase(BaseModel):
    id: str
    title: str
    description: str
    image_path: Optional[str] = Field(None, alias="imagePath")

    class Config:
        populate_by_name = True
        from_attributes = True


class HabitPlanResponse(HabitPlanBase):
    category: CategoryResponse
    suggestions: List[SuggestionResponse]
