from pydantic import BaseModel

__all__ = ("Response404", "Response409", "TaskCreatedResponse")


class Response404(BaseModel):
    message: str = "{item} not found"


class Response409(BaseModel):
    message: str = "failed to add {item}"


class TaskCreatedResponse(BaseModel):
    task_id: str
    task_status: str
    task_result: str | None
