from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.schemas.dish import DishBase, DishCreate, DishResponse
from src.models.models import Dish
from src.services.dish import DishService, get_dish_service

router = APIRouter()


@router.get(
    path='/dishes',
    summary='Список блюд',
    tags=['dishes'],
    response_model=list[DishResponse],
    status_code=status.HTTP_200_OK,
)
def dish_list(dish_service: DishService = Depends(get_dish_service)) -> list[DishResponse]:
    dishes: list = dish_service.get_dish_list()
    return [DishResponse(**dish.to_dict()) for dish in dishes]


@router.get(
    path='/dishes/{dish_id}',
    summary='Список подменю',
    tags=['dishes'],
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
def dish_detail(dish_id: int, dish_service: DishService = Depends(get_dish_service)) -> DishResponse:
    dish: Dish = dish_service.get_dish_by_id(dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
        )
    return DishResponse(**dish.to_dict())


@router.post(
    path='/dishes',
    summary='Добавить блюдо',
    tags=['dishes'],
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
)
def dish_create(menu_id: int, submenu_id: int, dish: DishCreate,
                dish_service: DishService = Depends(get_dish_service)) -> DishResponse:
    price = dish.price[:-1] if len(dish.price) - dish.price.find('.') != 3 else dish.price
    dish.price = price
    new_dish: Dish | None = dish_service.create_dish(menu_id=menu_id, submenu_id=submenu_id, new_dish=dish)
    if not new_dish:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='failed to add dish')
    return DishResponse(**new_dish.to_dict())


@router.patch(
    path='/dishes/{dish_id}',
    summary='Добавить подменю',
    tags=['dishes'],
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
def dish_update(dish_id: int, dish: DishBase, dish_service: DishService = Depends(get_dish_service)) -> DishResponse:
    updated_dish: Dish | None = dish_service.update_dish(dish_id=dish_id, updated_data=dish)
    if not updated_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
        )
    return DishResponse(**updated_dish.to_dict())


@router.delete(
    path='/dishes/{dish_id}',
    summary='Удалить подменю',
    tags=['dishes'],
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def dish_delete(menu_id: int, submenu_id: int, dish_id: int,
                dish_service: DishService = Depends(get_dish_service)) -> dict:
    success: bool = dish_service.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found',
        )
    return {'status': 'true', 'message': 'The dish has been deleted'}
