from pydantic import BaseModel

__all__ = (
    'SubMenuBase',
    'SubMenuCreate',
    'SubMenuResponse',
)


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    dishes_count: int = 0


class SubMenuResponse(SubMenuBase):
    id: str
    dishes_count: int = 0
