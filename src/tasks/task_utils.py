from fastapi.responses import JSONResponse


class TaskResponse(JSONResponse):
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
