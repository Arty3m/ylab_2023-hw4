import os.path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from src.api.v1.schemas import TaskCreatedResponse
from src.core import config
from src.services.full_menu import FullMenu, get_full_menu
from src.tasks import create_task, get_task_info
from src.tasks.task_utils import TaskResponse

router = APIRouter()


@router.post(
    path="/task",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["celery"],
    response_model=TaskCreatedResponse,
    summary="Создать excel файл",
    description="Добавление задачи на создание excel файла",
)
async def get_excel_f(full_menu: FullMenu = Depends(get_full_menu)):
    data = await full_menu.make_excel_file()
    task_id = create_task.delay(data)
    return get_task_info(task_id)


@router.get(
    path="/task/{task_id}",
    tags=["celery"],
    status_code=status.HTTP_200_OK,
    response_class=TaskResponse,
    summary="Получить excel файл",
    description="Получить excel файл по task_id",
)
async def get_task_status(task_id: str):
    """func that return file xlsx"""
    task_data = get_task_info(task_id)
    if not task_data.get("task_result"):
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=task_data,
        )
    path = os.path.join(config.BASE_DIR, f"{task_id}.xlsx")
    return FileResponse(
        path=path,
        filename="FullMenu.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get(
    path="/create_full_menu",
    tags=["fill_database"],
    status_code=status.HTTP_200_OK,
    summary="Заполнить БД",
    description="Заполнение БД начальными данными",
)
async def create_full_menu(full_menu: FullMenu = Depends(get_full_menu)):
    return await full_menu.create_all_menu()
