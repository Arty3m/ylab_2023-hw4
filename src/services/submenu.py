from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.submenu import SubMenuBase, SubMenuCreate
from src.db import get_db
from src.models import SubMenu, Menu
from src.services.mixins import ServiceMixin

__all__ = ('SubMenuService', 'get_submenu_service')


class SubMenuService(ServiceMixin):
    def get_submenu_list(self) -> list:
        return self.db.query(SubMenu).all()

    def get_submenu_by_id(self, submenu_id: int) -> SubMenu:
        submenu = self.db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
        return submenu

    def create_submenu(self, menu_id: int, new_submenu: SubMenuCreate) -> SubMenu | None:
        submenu: SubMenu = SubMenu(**new_submenu.dict())
        submenu.owner = menu_id
        if self.db.query(SubMenu).filter(SubMenu.title == new_submenu.title).first():
            return None

        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        menu.submenus_count += 1

        self.db.add(submenu)
        self.db.commit()
        self.db.refresh(submenu)
        return submenu

    def update_submenu(self, submenu_id: int, updated_data: SubMenuBase) -> SubMenu | None:
        submenu_to_upd: SubMenu = self.get_submenu_by_id(submenu_id=submenu_id)
        if not submenu_to_upd:
            return None
        submenu_to_upd.title = updated_data.title
        submenu_to_upd.description = updated_data.description
        self.db.add(submenu_to_upd)
        self.db.commit()
        self.db.refresh(submenu_to_upd)
        return submenu_to_upd

    def delete_submenu(self, menu_id: int, submenu_id: int) -> bool:
        to_del: SubMenu = self.get_submenu_by_id(submenu_id=submenu_id)
        if not to_del:
            return False
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        menu.submenus_count -= 1
        menu.dishes_count -= to_del.dishes_count
        self.db.delete(to_del)
        self.db.commit()
        return True


@lru_cache
def get_submenu_service(db: Session = Depends(get_db)) -> SubMenuService:
    return SubMenuService(db=db)
