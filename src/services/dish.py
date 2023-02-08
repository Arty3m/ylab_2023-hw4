import json
from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.dish import DishBase, DishCreate, DishResponse
from src.db import Redis, get_db, get_redis
from src.models import Dish, Menu, SubMenu
from src.services import CRUD

__all__ = ("DishService", "get_dish_service")


@dataclass
class DishService:
    cache: Redis
    crud: CRUD

    async def get_dish_list(self) -> list[DishResponse]:
        if from_cache := await self.cache.get("dish_list"):
            return json.loads(from_cache)

        data = await self.crud.get_all(Dish)
        dish_list: list[DishResponse] = [
            DishResponse(
                **dish.to_dict(),
            )
            for dish in data
        ]
        await self.cache.set("dish_list", json.dumps(jsonable_encoder(dish_list)), ex=60)
        return dish_list

    async def get_dish_by_id(self, dish_id: int) -> DishResponse:
        if from_cache := await self.cache.get(f"dish_{dish_id}"):
            return DishResponse(**json.loads(from_cache))

        dish: Dish = await self.crud.get_from_db_by_id(Dish, dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        serialized_data: dict = dish.to_dict()
        await self.cache.set(f"dish_{dish_id}", json.dumps(jsonable_encoder(serialized_data)), ex=60)
        return DishResponse(**serialized_data)

    async def create_dish(
        self,
        menu_id: int,
        submenu_id: int,
        new_dish: DishCreate,
    ) -> DishResponse:
        price = new_dish.price[:-1] if len(new_dish.price) - new_dish.price.find(".") != 3 else new_dish.price
        new_dish.price = price
        dish: Dish = Dish(**new_dish.dict())
        dish.owner = submenu_id

        if await self.crud.get_from_db_by_title(Dish, new_dish.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="failed to add dish",
            )
        menu: Menu = await self.crud.get_from_db_by_id(Menu, menu_id)
        submenu: SubMenu = await self.crud.get_from_db_by_id(SubMenu, submenu_id)
        menu.dishes_count += 1
        submenu.dishes_count += 1
        await self.crud.add_to_db(dish)

        serialized_data: dict = dish.to_dict()
        await self.cache.set(f"dish_{dish.id}", json.dumps(serialized_data), 300)
        await self.cache.delete(f"menu_{menu_id}")
        await self.cache.delete(f"submenu_{submenu_id}")
        await self.cache.delete("menu_list")
        await self.cache.delete("submenu_list")
        await self.cache.delete("dish_list")
        return DishResponse(**serialized_data)

    async def update_dish(self, dish_id: int, updated_data: DishBase) -> DishResponse:
        if not await self.crud.get_from_db_by_id(Dish, dish_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        updated: dict = await self.crud.update_data(dish_id, Dish, updated_data)
        await self.cache.delete(f"dish_{dish_id}")
        await self.cache.delete("dish_list")
        return DishResponse(**updated)

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> dict:
        to_del: Dish = await self.crud.get_from_db_by_id(Dish, dish_id)
        if not to_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        menu: Menu = await self.crud.get_from_db_by_id(Menu, menu_id)
        submenu: SubMenu = await self.crud.get_from_db_by_id(SubMenu, submenu_id)
        menu.dishes_count -= 1
        submenu.dishes_count -= 1
        await self.crud.delete_from_db(to_del)
        await self.cache.delete(f"menu_{menu_id}")
        await self.cache.delete(f"submenu_{submenu_id}")
        await self.cache.delete(f"dish_{dish_id}")
        await self.cache.delete("menu_list")
        await self.cache.delete("submenu_list")
        await self.cache.delete("dish_list")
        return {"status": "true", "message": "The dish has been deleted"}


@lru_cache
def get_dish_service(
    db: AsyncSession = Depends(get_db),
    cache=Depends(get_redis),
) -> DishService:
    crud: CRUD = CRUD(db)
    return DishService(crud=crud, cache=cache)
