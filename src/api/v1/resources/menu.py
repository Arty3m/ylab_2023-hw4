from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import (
    MenuBase,
    MenuCreate,
    MenuResponse,
    Response404,
    Response409,
)
from src.services.menu import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path='/menus',
    summary='Список меню',
    tags=['menus'],
    description='Получение списка меню',
    response_model=list[MenuResponse],
    status_code=status.HTTP_200_OK,
)
def menu_list(menu_service: MenuService = Depends(get_menu_service)) -> list[MenuResponse]:
    return menu_service.get_menu_list()


@router.get(
    path='/menus/{menu_id}',
    summary='Просмотр определенного меню',
    tags=['menus'],
    description='Получение определенного меню',
    responses={404: {'model': Response404}},
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
def menu_detail(menu_id: int, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    return menu_service.get_menu_by_id(menu_id=menu_id)


@router.post(
    path='/menus',
    summary='Добавить меню',
    tags=['menus'],
    description='Добавление нового меню',
    responses={409: {'model': Response409}},
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
)
def menu_create(menu: MenuCreate, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    return menu_service.create_menu(menu)


@router.patch(
    path='/menus/{menu_id}',
    summary='Обновить меню',
    tags=['menus'],
    description='Обновление заданного меню',
    responses={404: {'model': Response404}},
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
def menu_update(menu: MenuBase, menu_id: int, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    return menu_service.update_menu(menu_id, menu)


@router.delete(
    path='/menus/{menu_id}',
    summary='Удалить меню',
    tags=['menus'],
    description='Удаление заданного меню',
    responses={404: {'model': Response404}},
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def menu_delete(menu_id, menu_service: MenuService = Depends(get_menu_service)) -> dict:
    return menu_service.delete_menu(menu_id)
