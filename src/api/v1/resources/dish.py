from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import (
    DishBase,
    DishCreate,
    DishResponse,
    Response404,
    Response409,
)
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
    return dish_service.get_dish_list()


@router.get(
    path='/dishes/{dish_id}',
    summary='Просмотр определенного блюда',
    tags=['dishes'],
    description='Получение заданного блюда',
    responses={404: {'model': Response404}},
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
def dish_detail(dish_id: int, dish_service: DishService = Depends(get_dish_service)) -> DishResponse:
    return dish_service.get_dish_by_id(dish_id)


@router.post(
    path='/dishes',
    summary='Добавить блюдо',
    tags=['dishes'],
    description='Добавление нового блюда',
    responses={409: {'model': Response409}},
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
)
def dish_create(
        menu_id: int, submenu_id: int, dish: DishCreate,
        dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    return dish_service.create_dish(
        menu_id=menu_id, submenu_id=submenu_id, new_dish=dish,
    )


@router.patch(
    path='/dishes/{dish_id}',
    summary='Обновить блюдо',
    tags=['dishes'],
    description='Обновление заданного блюда',
    responses={404: {'model': Response404}},
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
def dish_update(dish_id: int, dish: DishBase, dish_service: DishService = Depends(get_dish_service)) -> DishResponse:
    return dish_service.update_dish(
        dish_id=dish_id, updated_data=dish,
    )


@router.delete(
    path='/dishes/{dish_id}',
    summary='Удалить блюдо',
    tags=['dishes'],
    description='Удаление заданного блюда',
    responses={404: {'model': Response404}},
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def dish_delete(
        menu_id: int, submenu_id: int, dish_id: int,
        dish_service: DishService = Depends(get_dish_service),
) -> dict:
    return dish_service.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
