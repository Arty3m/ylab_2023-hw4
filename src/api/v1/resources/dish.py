from fastapi import APIRouter, Depends, HTTPException

# vremeno tut
from src.db import get_db
from sqlalchemy.orm import Session
from src.models.menu import Dish
from src.api.v1.schemas.dish import DishCreate

###

router = APIRouter()


@router.get(
    path="/dishes",
    summary="Список блюд",
    tags=["dishes"],
    status_code=200,
)
def dish_list(db: Session = Depends(get_db)):
    dishs = db.query(Dish).all()
    return dishs


@router.get(
    path="/dishes/{dish_id}",
    summary="Список подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_detail(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return {"id": str(dish.id), "title": dish.title, "description": dish.description,
            "price": str(dish.price)}


@router.post(
    path="/dishes",
    summary="Добавить блюдо",
    tags=["dishes"],
    status_code=201,
)
def dish(submenu_id: int, dish_data: DishCreate, db: Session = Depends(get_db)):
    price = dish_data.price[:-1] if len(dish_data.price) - dish_data.price.find('.') != 3 else dish_data.price

    new_dish = Dish(title=dish_data.title, description=dish_data.description, price=price, owner=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return {"id": str(new_dish.id), "title": new_dish.title, "description": new_dish.description,
            "price": new_dish.price}


@router.patch(
    path="/dishes/{dish_id}",
    summary="Добавить подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_update(dish_id: int, dish_data: DishCreate, db: Session = Depends(get_db)):
    dish_to_change = db.get(Dish, dish_id)
    if not dish_to_change:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_to_change.title = dish_data.title
    dish_to_change.description = dish_data.description
    dish_to_change.price = dish_data.price
    db.add(dish_to_change)
    db.commit()
    db.refresh(dish_to_change)
    return {"id": str(dish_to_change.id), "title": dish_to_change.title,
            "description": dish_to_change.description, "price": dish_to_change.price}


@router.delete(
    path="/dishes/{dish_id}",
    summary="Удалить подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_delete(dish_id: int, db: Session = Depends(get_db)):
    to_del = db.get(Dish, dish_id)
    if not to_del:
        raise HTTPException(status_code=404, detail="dish not found")
    db.delete(to_del)
    db.commit()
    return {"status": "true", "message": "The dish has been deleted"}
