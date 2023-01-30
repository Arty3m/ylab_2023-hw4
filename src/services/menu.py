import json
import pickle
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.api.v1.schemas.menu import MenuBase, MenuCreate, MenuResponse
from src.db import get_db, get_redis
from src.models import Menu
from src.services import (
    ServiceMixin,
    add_to_db,
    delete_from_db,
    get_all,
    get_from_db_by_id,
    get_from_db_by_title,
    update_data,
)

__all__ = ('MenuService', 'get_menu_service')


class MenuService(ServiceMixin):
    def get_menu_list(self) -> list[MenuResponse]:
        if from_cache := self.cache.lrange('menu_list', 0, -1):
            print('FROM CACHE')
            return pickle.loads(from_cache[1])
        menu_list: list[MenuResponse] = [
            MenuResponse(
                **menu.to_dict(),
            ) for menu in get_all(self.db, Menu)
        ]
        self.cache.lpush('menu_list', pickle.dumps(menu_list), 300)
        return menu_list

    def get_menu_by_id(self, menu_id: int) -> MenuResponse:
        if from_cache := self.cache.get(f'menu_{menu_id}'):
            print('FROM CACHE')
            return MenuResponse(**json.loads(from_cache.decode('utf-8')))
        menu: Menu = get_from_db_by_id(self.db, Menu, menu_id)

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
            )
        serialized_data: dict = menu.to_dict()
        self.cache.set(f'menu_{menu_id}', json.dumps(serialized_data), 300)
        return MenuResponse(**serialized_data)

    def create_menu(self, new_menu: MenuCreate) -> MenuResponse:
        if get_from_db_by_title(self.db, Menu, new_menu.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='failed to add menu',
            )
        menu: Menu = Menu(**new_menu.dict())
        add_to_db(self.db, menu)
        serialized_data: dict = menu.to_dict()
        self.cache.set(f'menu_{menu.id}', json.dumps(serialized_data), 300)
        self.cache.delete('menu_list')
        return MenuResponse(**serialized_data)

    def update_menu(self, menu_id: int, updated_data: MenuBase) -> MenuResponse:
        menu_to_upd: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        if not menu_to_upd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
            )
        update_data(self.db, menu_to_upd, updated_data)
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete('menu_list')
        return MenuResponse(**menu_to_upd.to_dict())

    def delete_menu(self, menu_id: int) -> dict:
        to_del: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        if not to_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
            )
        delete_from_db(self.db, to_del)
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete('menu_list')
        self.cache.delete('submenu_list')
        self.cache.delete('dish_list')

        return {'status': 'true', 'message': 'The menu has been deleted'}


@lru_cache
def get_menu_service(db: Session = Depends(get_db), cache=Depends(get_redis)) -> MenuService:
    return MenuService(db=db, cache=cache)
