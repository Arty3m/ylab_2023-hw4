from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.menu import MenuBase, MenuCreate
from src.db import get_db
from src.models import Menu
from src.services.mixins import ServiceMixin

__all__ = ('MenuService', 'get_menu_service')


class MenuService(ServiceMixin):
    def get_menu_list(self) -> list:
        return self.db.query(Menu).all()

    def get_menu_by_id(self, menu_id: int) -> Menu:
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        return menu

    def create_menu(self, new_menu: MenuCreate) -> Menu | None:
        menu: Menu = Menu(**new_menu.dict())
        if self.db.query(Menu).filter(Menu.title == new_menu.title).first():
            return None
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def update_menu(self, menu_id: int, updated_data: MenuBase) -> Menu | None:
        menu_to_upd: Menu = self.get_menu_by_id(menu_id=menu_id)
        if not menu_to_upd:
            return None
        menu_to_upd.title = updated_data.title
        menu_to_upd.description = updated_data.description
        self.db.add(menu_to_upd)
        self.db.commit()
        self.db.refresh(menu_to_upd)
        return menu_to_upd

    def delete_menu(self, menu_id: int) -> bool:
        to_del: Menu = self.get_menu_by_id(menu_id=menu_id)
        if not to_del:
            return False
        self.db.delete(to_del)
        self.db.commit()
        return True


@lru_cache
def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(db=db)
