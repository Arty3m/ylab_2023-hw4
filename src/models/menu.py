from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    child = relationship("SubMenu", cascade='all,delete', backref='Menu')


class SubMenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    owner = Column(Integer, ForeignKey("menu.id", ondelete="CASCADE"))
    child = relationship("Dish", cascade='all,delete', backref='SubMenu')


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(String)
    owner = Column(Integer, ForeignKey("submenu.id", ondelete="CASCADE"))
