import json
import pickle
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.api.v1.schemas.submenu import SubMenuBase, SubMenuCreate, SubMenuResponse
from src.db import get_db, get_redis
from src.models import Menu, SubMenu
from src.services import (
    ServiceMixin,
    add_to_db,
    delete_from_db,
    get_all,
    get_from_db_by_id,
    get_from_db_by_title,
    update_data,
)

__all__ = ('SubMenuService', 'get_submenu_service')


class SubMenuService(ServiceMixin):
    def get_submenu_list(self) -> list[SubMenuResponse]:
        if from_cache := self.cache.lrange('submenu_list', 0, -1):
            print('FROM CACHE')
            return pickle.loads(from_cache[1])
        submenu_list: list[SubMenuResponse] = [
            SubMenuResponse(**submenu.to_dict()) for submenu in
            get_all(self.db, SubMenu)
        ]
        self.cache.lpush('submenu_list', pickle.dumps(submenu_list), 300)
        return submenu_list

    def get_submenu_by_id(self, submenu_id: int) -> SubMenuResponse:
        if from_cache := self.cache.get(f'submenu_{submenu_id}'):
            print('FROM CACHE')
            return SubMenuResponse(**json.loads(from_cache.decode('utf-8')))
        submenu: SubMenu = get_from_db_by_id(self.db, SubMenu, submenu_id)

        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
            )
        serialized_data: dict = submenu.to_dict()
        self.cache.set(
            f'submenu_{submenu_id}',
            json.dumps(serialized_data), 300,
        )
        return SubMenuResponse(**serialized_data)

    def create_submenu(self, menu_id: int, new_submenu: SubMenuCreate) -> SubMenuResponse:
        if get_from_db_by_title(self.db, SubMenu, new_submenu.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='failed to add submenu',
            )
        submenu: SubMenu = SubMenu(**new_submenu.dict())
        submenu.owner = menu_id
        menu: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        menu.submenus_count += 1

        add_to_db(self.db, submenu)
        serialized_data: dict = submenu.to_dict()
        self.cache.set(
            f'submenu_{submenu.id}',
            json.dumps(serialized_data), 300,
        )
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete('menu_list')
        self.cache.delete('submenu_list')
        return SubMenuResponse(**serialized_data)

    def update_submenu(self, submenu_id: int, updated_data: SubMenuBase) -> SubMenuResponse:
        submenu_to_upd: SubMenu = get_from_db_by_id(
            self.db, SubMenu, submenu_id,
        )
        if not submenu_to_upd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
            )

        update_data(self.db, submenu_to_upd, updated_data)
        self.cache.delete(f'submenu_{submenu_id}')
        self.cache.delete('submenu_list')
        return SubMenuResponse(**submenu_to_upd.to_dict())

    def delete_submenu(self, menu_id: int, submenu_id: int) -> dict:
        to_del: SubMenu = get_from_db_by_id(self.db, SubMenu, submenu_id)
        if not to_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
            )
        menu: Menu = get_from_db_by_id(self.db, Menu, menu_id)
        menu.submenus_count -= 1
        menu.dishes_count -= to_del.dishes_count
        self.cache.delete(f'submenu_{submenu_id}')
        self.cache.delete(f'menu_{menu_id}')
        self.cache.delete('menu_list')
        self.cache.delete('submenu_list')
        self.cache.delete('dish_list')
        delete_from_db(self.db, to_del)
        return {'status': 'true', 'message': 'The submenu has been deleted'}


@lru_cache
def get_submenu_service(db: Session = Depends(get_db), cache=Depends(get_redis)) -> SubMenuService:
    return SubMenuService(db=db, cache=cache)
