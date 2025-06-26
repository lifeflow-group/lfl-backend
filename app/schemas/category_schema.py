from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    icon_path: Optional[str] = Field(None, alias="iconPath")  # camelCase alias
    color_hex: Optional[str] = Field(None, alias="colorHex")  # camelCase alias

    class Config:
        populate_by_name = True


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: str

    class Config:
        from_attributes = True
