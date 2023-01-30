import json
import pickle
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.api.v1.schemas.dish import DishBase, DishCreate, DishResponse
from src.db import get_db, get_redis
from src.models import Dish, Menu, SubMenu
from src.services import (
    ServiceMixin,
    add_to_db,
    delete_from_db,
    get_all,
    get_from_db_by_id,
    get_from_db_by_title,
    update_data,
)

__all__ = ('DishService', 'get_dish_service')


class DishService(ServiceMixin):
    def get_dish_list(self) -> list[DishResponse]:
        if from_cache := self.cache.lrange('dish_list', 0, -1):
            print('FROM CACHE')
            return pickle.loads(from_cache[1])
        dish_list: list[DishResponse] = [
            DishResponse(
                **dish.to_dict(),
            ) for dish in get_all(self.db, Dish)
        ]
        self.cache.lpush('dish_list', pickle.dumps(dish_list), 300)
        return dish_list

    def get_dish_by_id(self, dish_id: int) -> DishResponse:
        if from_cache := self.cache.get(f'dish_{dish_id}'):
            print('FROM CACHE')
            return DishResponse(**json.loads(from_cache.decode('utf-8')))

        dish: Dish = get_from_db_by_id(self.db, Dish, dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
            )
        serialized_data: dict = dish.to_dict()
        self.cache.set(f'dish_{dish_id}', json.dumps(serialized_data), 300)
        return DishResponse(**serialized_data)

    def create_dish(self, menu_id: int, submenu_id: int, new_dish: DishCreate) -> DishResponse:
        price = new_dish.price[:-1] if len(new_dish.price) - \
            new_dish.price.find('.') != 3 else new_dish.price
        new_dish.price = price

        if get_from_db_by_title(self.db, Dish, new_dish.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='failed to add dish',
            )
        dish: Dish = Dish(**new_dish.dict())
        dish.owner = submenu_id

        menu: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        submenu: SubMenu = get_from_db_by_id(self.db, SubMenu, submenu_id)
        menu.dishes_count += 1
        submenu.dishes_count += 1
        add_to_db(self.db, dish)

        serialized_data: dict = dish.to_dict()
        self.cache.set(f'dish_{dish.id}', json.dumps(serialized_data), 300)
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete(f'submenu_{submenu_id}')
        self.cache.delete('menu_list')
        self.cache.delete('submenu_list')
        self.cache.delete('dish_list')
        return DishResponse(**serialized_data)

    def update_dish(self, dish_id: int, updated_data: DishBase) -> DishResponse:
        dish_to_upd: Dish = get_from_db_by_id(self.db, Dish, dish_id)
        if not dish_to_upd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
            )
        update_data(self.db, dish_to_upd, updated_data)
        self.cache.delete(f'dish_{dish_id}')
        self.cache.delete('dish_list')
        return DishResponse(**dish_to_upd.to_dict())

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> dict:
        to_del: Dish = get_from_db_by_id(self.db, Dish, dish_id)
        if not to_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
            )
        menu: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        submenu: SubMenu = get_from_db_by_id(self.db, SubMenu, submenu_id)
        menu.dishes_count -= 1
        submenu.dishes_count -= 1
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete(f'submenu_{submenu_id}')
        self.cache.delete(f'dish_{dish_id}')
        self.cache.delete('menu_list')
        self.cache.delete('submenu_list')
        self.cache.delete('dish_list')
        delete_from_db(self.db, to_del)
        return {'status': 'true', 'message': 'The dish has been deleted'}


@lru_cache
def get_dish_service(db: Session = Depends(get_db), cache=Depends(get_redis)) -> DishService:
    return DishService(db=db, cache=cache)
