import os

from celery.result import AsyncResult
from openpyxl.workbook import Workbook

from src.core import config
from src.tasks import celery


@celery.task  # type: ignore
def create_task(data):
    task_id = celery.current_task.request.id  # type: ignore
    filename = f"{task_id}.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Меню"
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            ws.cell(i + 1, j + 1, el)
    wb.save(os.path.join(config.BASE_DIR, filename))
    return task_id


def get_task_info(task_id: str) -> dict:
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_result.id.__str__(),
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result
