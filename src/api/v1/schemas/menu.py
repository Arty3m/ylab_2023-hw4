from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "MenuBase",
    "MenuCreate",
    "MenuModel"
)


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    ...


class MenuModel(MenuBase):
    id: str


class MenuCreated(MenuModel):
    count_submenus: int
    count_dishes: int
