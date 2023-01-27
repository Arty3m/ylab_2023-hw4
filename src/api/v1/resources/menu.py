from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.schemas.menu import MenuBase, MenuCreate, MenuResponse
from src.models import Menu
from src.services.menu import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path='/menus',
    summary='Список меню',
    tags=['menus'],
    response_model=list[MenuResponse],
    status_code=status.HTTP_200_OK,
)
def menu_list(menu_service: MenuService = Depends(get_menu_service)) -> list[MenuResponse]:
    m_list: list = menu_service.get_menu_list()
    return [MenuResponse(**menu.to_dict()) for menu in m_list]


@router.get(
    path='/menus/{menu_id}',
    summary='Просмотр определенного меню',
    tags=['menus'],
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
def menu_detail(menu_id: int, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    menu: Menu = menu_service.get_menu_by_id(menu_id=menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
        )
    return MenuResponse(**menu.to_dict())


@router.post(
    path='/menus',
    summary='Добавить меню',
    tags=['menus'],
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
)
def menu_create(menu: MenuCreate, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    new_menu: Menu = menu_service.create_menu(menu)
    if not new_menu:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='menu already exist')
    return MenuResponse(**new_menu.to_dict())


@router.patch(
    path='/menus/{menu_id}',
    summary='Обновить меню',
    tags=['menus'],
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
def menu_update(menu: MenuBase, menu_id: int, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    updated_menu: Menu | None = menu_service.update_menu(menu_id, menu)
    if not updated_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
        )

    return MenuResponse(**updated_menu.to_dict())


#
@router.delete(
    path='/menus/{menu_id}',
    summary='Удалить меню',
    tags=['menus'],
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def menu_delete(menu_id, menu_service: MenuService = Depends(get_menu_service)) -> dict:
    success = menu_service.delete_menu(menu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu not found',
        )
    return {'status': 'true', 'message': 'The menu has been deleted'}
