from pydantic import BaseModel, Field
from typing import Optional


class HabitCategoryBase(BaseModel):
    label: str
    icon_path: Optional[str] = Field(None, alias="iconPath")  # camelCase alias

    class Config:
        populate_by_name = True


class HabitCategoryCreate(HabitCategoryBase):
    pass


class HabitCategoryResponse(HabitCategoryBase):
    id: str

    class Config:
        from_attributes = True
