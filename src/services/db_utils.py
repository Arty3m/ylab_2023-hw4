from sqlalchemy import select, update
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas import DishBase, MenuBase, SubMenuBase
from src.models import Dish, Menu, SubMenu

__all__ = (
    "add_to_db",
    "get_all",
    "get_from_db_by_id",
    "get_from_db_by_title",
    "delete_from_db",
    "update_data",
)


async def add_to_db(db: AsyncSession, item: Menu | SubMenu | Dish):
    db.add(item)
    await db.commit()
    await db.refresh(item)


async def get_all(db: AsyncSession, entity: type[Menu | SubMenu | Dish]):
    query = select(entity)
    data: Row = await db.execute(query)
    d = data.scalars().all()
    return d


async def get_from_db_by_id(
    db: AsyncSession,
    entity: type[Menu | SubMenu | Dish],
    required_id: int,
):
    query = select(entity).where(entity.id == required_id)
    data: Row = await db.execute(query)
    d = data.fetchone()
    return [] if not d else d[0]


async def get_from_db_by_title(
    db: AsyncSession,
    entity: type[Menu | SubMenu | Dish],
    title: str,
):
    query = select(entity).where(entity.title == title)
    data: Row = await db.execute(query)
    return data.fetchone()


async def update_data(
    db: AsyncSession,
    required_id: int,
    entity: type[Menu | SubMenu | Dish],
    updated_data: DishBase | MenuBase | SubMenuBase,
):
    upd_data = updated_data.dict()
    query = update(entity).where(entity.id == required_id).values(**upd_data).returning(entity)
    data: Row = await db.execute(query)
    await db.commit()
    return dict(data.fetchone())


async def delete_from_db(db: AsyncSession, item: Menu | SubMenu | Dish):
    await db.delete(item)
    await db.commit()
