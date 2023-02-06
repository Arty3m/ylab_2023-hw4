from pydantic import BaseModel

__all__ = (
    "MenuBase",
    "MenuCreate",
    "MenuResponse",
)


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuResponse(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int
