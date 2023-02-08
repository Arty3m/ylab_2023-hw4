from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas import DishBase, MenuBase, SubMenuBase
from src.models import Dish, Menu, SubMenu

__all__ = ("CRUD",)


@dataclass
class CRUD:
    db: AsyncSession

    async def add_to_db(self, item: Menu | SubMenu | Dish):
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)

    async def get_all(self, entity: type[Menu | SubMenu | Dish]):
        query = select(entity)
        data: Row = await self.db.execute(query)
        d = data.scalars().all()
        return d

    async def get_from_db_by_id(
        self,
        entity: type[Menu | SubMenu | Dish],
        required_id: int,
    ):
        query = select(entity).where(entity.id == required_id)
        data: Row = await self.db.execute(query)
        d = data.fetchone()
        return [] if not d else d[0]

    async def get_from_db_by_title(
        self,
        entity: type[Menu | SubMenu | Dish],
        title: str,
    ):
        query = select(entity).where(entity.title == title)
        data: Row = await self.db.execute(query)
        return data.fetchone()

    async def update_data(
        self,
        required_id: int,
        entity: type[Menu | SubMenu | Dish],
        updated_data: DishBase | MenuBase | SubMenuBase,
    ):
        upd_data = updated_data.dict()
        query = update(entity).where(entity.id == required_id).values(**upd_data).returning(entity)
        data: Row = await self.db.execute(query)
        await self.db.commit()
        return dict(data.fetchone())

    async def delete_from_db(self, item: Menu | SubMenu | Dish):
        await self.db.delete(item)
        await self.db.commit()

    async def get_full_menu(self, query: str):
        data = await self.db.execute(query)
        return data.fetchall()
