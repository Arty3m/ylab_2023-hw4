from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.schemas.submenu import SubMenuBase, SubMenuCreate, SubMenuResponse
from src.models.models import SubMenu
from src.services.submenu import SubMenuService, get_submenu_service

router = APIRouter()


@router.get(
    path='/submenus',
    summary='Список подменю',
    tags=['submenus'],
    response_model=list[SubMenuResponse],
    status_code=status.HTTP_200_OK,
)
def submenu_list(submenu_service: SubMenuService = Depends(get_submenu_service)) -> list[SubMenuResponse]:
    submenus: list = submenu_service.get_submenu_list()
    return [SubMenuResponse(**submenu.to_dict()) for submenu in submenus]


@router.get(
    path='/submenus/{submenu_id}',
    summary='Список подменю',
    tags=['submenus'],
    response_model=SubMenuResponse,
    status_code=status.HTTP_200_OK,
)
def submenu_detail(submenu_id: int, submenu_service: SubMenuService = Depends(get_submenu_service)) -> SubMenuResponse:
    submenu: SubMenu = submenu_service.get_submenu_by_id(submenu_id=submenu_id)
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
        )
    return SubMenuResponse(**submenu.to_dict())


@router.post(
    path='/submenus',
    summary='Добавить подменю',
    tags=['submenus'],
    response_model=SubMenuResponse,
    status_code=status.HTTP_201_CREATED,
)
def submenu_create(menu_id: int, sub_menu: SubMenuCreate,
                   submenu_service: SubMenuService = Depends(get_submenu_service)) -> SubMenuResponse:
    new_submenu: SubMenu | None = submenu_service.create_submenu(menu_id=menu_id, new_submenu=sub_menu)
    if not new_submenu:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='failed to add submenu')
    return SubMenuResponse(**new_submenu.to_dict())


@router.patch(
    path='/submenus/{submenu_id}',
    summary='Добавить подменю',
    tags=['submenus'],
    response_model=SubMenuResponse,
    status_code=status.HTTP_200_OK,
)
def submenu_update(submenu_id: int, sub_menu: SubMenuBase,
                   submenu_service: SubMenuService = Depends(get_submenu_service)) -> SubMenuResponse:
    updated_submenu: SubMenu | None = submenu_service.update_submenu(submenu_id, sub_menu)
    if not updated_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
        )
    return SubMenuResponse(**updated_submenu.to_dict())


@router.delete(
    path='/submenus/{submenu_id}',
    summary='Удалить подменю',
    tags=['submenus'],
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def submenu_delete(menu_id: int, submenu_id: int,
                   submenu_service: SubMenuService = Depends(get_submenu_service)) -> dict:
    success: bool = submenu_service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found',
        )
    return {'status': 'true', 'message': 'The submenu has been deleted'}
