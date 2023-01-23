from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "DishBase",
    "DishCreate",
    "DishModel"
)


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    ...


class DishModel(DishBase):
    id: str
