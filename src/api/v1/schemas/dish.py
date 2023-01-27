from pydantic import BaseModel

__all__ = (
    'DishBase',
    'DishCreate',
    'DishResponse',
)


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    ...


class DishResponse(DishBase):
    id: str
