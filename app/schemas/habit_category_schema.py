from pydantic import BaseModel, Field
from typing import Optional


class HabitCategoryBase(BaseModel):
    name: str
    icon_path: Optional[str] = Field(None, alias="iconPath")  # camelCase alias
    color_hex: Optional[str] = Field(None, alias="colorHex")  # camelCase alias

    class Config:
        populate_by_name = True


class HabitCategoryCreate(HabitCategoryBase):
    pass


class HabitCategoryResponse(HabitCategoryBase):
    id: str

    class Config:
        from_attributes = True
