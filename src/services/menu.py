import json
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.api.v1.schemas.menu import MenuBase, MenuCreate, MenuResponse
from src.db import get_db, get_redis, Redis
from src.models import Menu
from src.services import CRUD


__all__ = ("MenuService", "get_menu_service")


@dataclass
class MenuService:
    cache: Redis
    crud: CRUD

    async def get_menu_list(self) -> list[MenuResponse]:
        if from_cache := await self.cache.get("menu_list"):
            return json.loads(from_cache)

        data = await self.crud.get_all(Menu)
        menu_list: list[MenuResponse] = [
            MenuResponse(
                **menu.to_dict(),
            )
            for menu in data
        ]
        await self.cache.set("menu_list", json.dumps(jsonable_encoder(menu_list)), ex=60)
        return menu_list

    async def get_menu_by_id(self, menu_id: int) -> MenuResponse:
        if from_cache := await self.cache.get(f"menu_{menu_id}"):
            return MenuResponse(**json.loads(from_cache))

        menu: Menu = await self.crud.get_from_db_by_id(Menu, menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        serialized_data: dict = menu.to_dict()
        await self.cache.set(f"menu_{menu_id}", json.dumps(jsonable_encoder(serialized_data)), ex=60)
        return MenuResponse(**serialized_data)

    async def create_menu(self, new_menu: MenuCreate) -> MenuResponse:
        menu: Menu = Menu(**new_menu.dict())
        if await self.crud.get_from_db_by_title(Menu, new_menu.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="failed to add menu",
            )
        # await add_to_db(self.db, menu)
        await self.crud.add_to_db(menu)
        serialized_data: dict = menu.to_dict()
        await self.cache.set(f"menu_{menu.id}", json.dumps(serialized_data), ex=300)
        await self.cache.delete("menu_list")
        return MenuResponse(**serialized_data)

    async def update_menu(self, menu_id: int, updated_data: MenuBase) -> MenuResponse:
        if not await self.crud.get_from_db_by_id(Menu, menu_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        updated: dict = await self.crud.update_data(menu_id, Menu, updated_data)
        await self.cache.delete(f"menu_{menu_id}")
        await self.cache.delete("menu_list")
        return MenuResponse(**updated)

    async def delete_menu(self, menu_id: int) -> dict:
        menu: Menu = await self.crud.get_from_db_by_id(Menu, int(menu_id))
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        await self.crud.delete_from_db(menu)
        await self.cache.flushdb()

        return {"status": "true", "message": "The menu has been deleted"}


@lru_cache
def get_menu_service(
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis),
) -> MenuService:
    crud: CRUD = CRUD(db)
    return MenuService(crud=crud, cache=cache)
