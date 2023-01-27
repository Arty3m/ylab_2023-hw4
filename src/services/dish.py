from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.dish import DishBase, DishCreate
from src.db import get_db
from src.models import Dish, SubMenu, Menu
from src.services.mixins import ServiceMixin

__all__ = ('DishService', 'get_dish_service')


class DishService(ServiceMixin):
    def get_dish_list(self) -> list:
        return self.db.query(Dish).all()

    def get_dish_by_id(self, dish_id: int) -> Dish:
        dish = self.db.query(Dish).filter(Dish.id == dish_id).first()
        return dish

    def create_dish(self, menu_id: int, submenu_id: int, new_dish: DishCreate) -> Dish | None:
        dish: Dish = Dish(**new_dish.dict())
        dish.owner = submenu_id

        if self.db.query(Dish).filter(Dish.title == new_dish.title).first():
            return None

        menu: Menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        menu.dishes_count += 1
        submenu: SubMenu = self.db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
        submenu.dishes_count += 1

        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)
        return dish

    def update_dish(self, dish_id: int, updated_data: DishBase) -> Dish | None:
        dish_to_upd: Dish = self.get_dish_by_id(dish_id=dish_id)
        if not dish_to_upd:
            return None
        dish_to_upd.title = updated_data.title
        dish_to_upd.description = updated_data.description
        dish_to_upd.price = updated_data.price
        self.db.add(dish_to_upd)
        self.db.commit()
        self.db.refresh(dish_to_upd)
        return dish_to_upd

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> bool:
        to_del: Dish = self.get_dish_by_id(dish_id=dish_id)
        if not to_del:
            return False
        menu: Menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        menu.dishes_count -= 1
        submenu: SubMenu = self.db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
        submenu.dishes_count -= 1
        self.db.delete(to_del)
        self.db.commit()
        return True


@lru_cache
def get_dish_service(db: Session = Depends(get_db)) -> DishService:
    return DishService(db=db)
