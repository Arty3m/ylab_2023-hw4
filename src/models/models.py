from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)
    child = relationship('SubMenu', cascade='all,delete', backref='Menu')

    def to_dict(self):
        return {key: getattr(self, key) for key in vars(self) if key != '_sa_instance_state'}


class SubMenu(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    dishes_count = Column(Integer, default=0)
    owner = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'))

    child = relationship('Dish', cascade='all,delete', backref='SubMenu')

    def to_dict(self):
        return {key: getattr(self, key) for key in vars(self) if key != '_sa_instance_state'}


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(String)

    owner = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'))

    def to_dict(self):
        return {key: getattr(self, key) for key in vars(self) if key != '_sa_instance_state'}
