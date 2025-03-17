from pydantic import BaseModel
from typing import Optional

class HabitCategoryBase(BaseModel):
    label: str
    icon_path: Optional[str]

class HabitCategoryCreate(HabitCategoryBase):
    pass

class HabitCategoryResponse(HabitCategoryBase):
    id: str

    class Config:
        from_attributes = True
