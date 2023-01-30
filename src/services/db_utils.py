from sqlmodel import Session

from src.api.v1.schemas import DishBase, MenuBase, SubMenuBase
from src.models import Dish, Menu, SubMenu

__all__ = (
    'add_to_db', 'get_all', 'get_from_db_by_id',
    'get_from_db_by_title', 'delete_from_db', 'update_data',
)


def add_to_db(db: Session, item: Menu | SubMenu | Dish):
    db.add(item)
    db.commit()
    db.refresh(item)


def get_all(db: Session, entity: type[Menu | SubMenu | Dish]):
    return db.query(entity).all()


def get_from_db_by_id(db: Session, entity: type[Menu | SubMenu | Dish], required_id: int):
    return db.query(entity).filter(entity.id == required_id).first()


def get_from_db_by_title(db: Session, entity: type[Menu | SubMenu | Dish], title: str):
    return db.query(entity).filter(entity.title == title).first()


def update_data(db: Session, obj_to_upd: Menu | SubMenu | Dish, updated_data: DishBase | MenuBase | SubMenuBase):
    upd_data = updated_data.dict()
    for key in upd_data:
        setattr(obj_to_upd, key, upd_data[key])
    add_to_db(db, obj_to_upd)


def delete_from_db(db: Session, item: Menu | SubMenu | Dish):
    db.delete(item)
    db.commit()
