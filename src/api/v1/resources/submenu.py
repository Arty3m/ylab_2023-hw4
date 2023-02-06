from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import (
    Response404,
    Response409,
    SubMenuBase,
    SubMenuCreate,
    SubMenuResponse,
)
from src.services.submenu import SubMenuService, get_submenu_service

router = APIRouter()


@router.get(
    path="/submenus",
    summary="Список подменю",
    tags=["submenus"],
    description="Получение списка подменю",
    response_model=list[SubMenuResponse],
    status_code=status.HTTP_200_OK,
)
async def submenu_list(
    submenu_service: SubMenuService = Depends(get_submenu_service),
) -> list[SubMenuResponse]:
    return await submenu_service.get_submenu_list()


@router.get(
    path="/submenus/{submenu_id}",
    summary="Просмотр определенного подменю",
    tags=["submenus"],
    description="Получение определенного подменю",
    responses={404: {"model": Response404}},
    response_model=SubMenuResponse,
    status_code=status.HTTP_200_OK,
)
async def submenu_detail(
    submenu_id: int,
    submenu_service: SubMenuService = Depends(get_submenu_service),
) -> SubMenuResponse:
    return await submenu_service.get_submenu_by_id(submenu_id=submenu_id)


@router.post(
    path="/submenus",
    summary="Добавить подменю",
    tags=["submenus"],
    description="Создание нового подменю",
    responses={409: {"model": Response409}},
    response_model=SubMenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submenu_create(
    menu_id: int,
    sub_menu: SubMenuCreate,
    submenu_service: SubMenuService = Depends(get_submenu_service),
) -> SubMenuResponse:
    return await submenu_service.create_submenu(menu_id=menu_id, new_submenu=sub_menu)


@router.patch(
    path="/submenus/{submenu_id}",
    summary="Обновить подменю",
    tags=["submenus"],
    description="Обновление заданного подменю",
    responses={404: {"model": Response404}},
    response_model=SubMenuResponse,
    status_code=status.HTTP_200_OK,
)
async def submenu_update(
    submenu_id: int,
    sub_menu: SubMenuBase,
    submenu_service: SubMenuService = Depends(get_submenu_service),
) -> SubMenuResponse:
    return await submenu_service.update_submenu(submenu_id, sub_menu)


@router.delete(
    path="/submenus/{submenu_id}",
    summary="Удалить подменю",
    tags=["submenus"],
    description="Удаление заданного подменю",
    responses={404: {"model": Response404}},
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def submenu_delete(
    menu_id: int,
    submenu_id: int,
    submenu_service: SubMenuService = Depends(get_submenu_service),
) -> dict:
    return await submenu_service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
