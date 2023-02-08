import json
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.api.v1.schemas.submenu import SubMenuBase, SubMenuCreate, SubMenuResponse
from src.db import get_db, get_redis, Redis
from src.models import Menu, SubMenu
from src.services import CRUD

__all__ = ("SubMenuService", "get_submenu_service")


@dataclass
class SubMenuService:
    cache: Redis
    crud: CRUD

    async def get_submenu_list(self) -> list[SubMenuResponse]:
        if from_cache := await self.cache.get("submenu_list"):
            return json.loads(from_cache)
        data = await self.crud.get_all(SubMenu)
        submenu_list: list[SubMenuResponse] = [SubMenuResponse(**submenu.to_dict()) for submenu in data]
        await self.cache.set("submenu_list", json.dumps(jsonable_encoder(submenu_list)), ex=60)
        return submenu_list

    async def get_submenu_by_id(self, submenu_id: int) -> SubMenuResponse:
        if from_cache := await self.cache.get(f"submenu_{submenu_id}"):
            return SubMenuResponse(**json.loads(from_cache))

        submenu: SubMenu = await self.crud.get_from_db_by_id(SubMenu, submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        serialized_data: dict = submenu.to_dict()
        await self.cache.set(
            f"submenu_{submenu_id}",
            json.dumps(jsonable_encoder(serialized_data)),
            ex=60,
        )
        return SubMenuResponse(**serialized_data)

    async def create_submenu(
            self,
            menu_id: int,
            new_submenu: SubMenuCreate,
    ) -> SubMenuResponse:
        submenu: SubMenu = SubMenu(**new_submenu.dict())
        submenu.owner = menu_id

        if await self.crud.get_from_db_by_title(SubMenu, new_submenu.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="failed to add submenu",
            )
        menu: Menu = await self.crud.get_from_db_by_id(Menu, menu_id)
        menu.submenus_count += 1
        await self.crud.add_to_db(submenu)
        serialized_data: dict = submenu.to_dict()
        await self.cache.set(
            f"submenu_{submenu.id}",
            json.dumps(serialized_data),
            ex=60,
        )
        await self.cache.delete(f"menu_{menu_id}")
        await self.cache.delete("menu_list")
        await self.cache.delete("submenu_list")
        return SubMenuResponse(**serialized_data)

    async def update_submenu(
            self,
            submenu_id: int,
            updated_data: SubMenuBase,
    ) -> SubMenuResponse:
        if not await self.crud.get_from_db_by_id(SubMenu, submenu_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        updated: dict = await self.crud.update_data(submenu_id, SubMenu, updated_data)
        await self.cache.delete(f"submenu_{submenu_id}")
        await self.cache.delete("submenu_list")
        return SubMenuResponse(**updated)

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> dict:
        to_del: SubMenu = await self.crud.get_from_db_by_id(SubMenu, submenu_id)
        if not to_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        menu: Menu = await self.crud.get_from_db_by_id(Menu, menu_id)
        menu.submenus_count -= 1
        menu.dishes_count -= to_del.dishes_count
        await self.crud.delete_from_db(to_del)
        await self.cache.delete(f"submenu_{submenu_id}")
        await self.cache.delete(f"menu_{menu_id}")
        await self.cache.delete("menu_list")
        await self.cache.delete("submenu_list")
        await self.cache.delete("dish_list")
        return {"status": "true", "message": "The submenu has been deleted"}


@lru_cache
def get_submenu_service(
        db: AsyncSession = Depends(get_db),
        cache=Depends(get_redis),
) -> SubMenuService:
    crud: CRUD = CRUD(db)
    return SubMenuService(crud=crud, cache=cache)
