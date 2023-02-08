import uvicorn
from fastapi import FastAPI, status

from src.api.v1.resources import dish, full_menu, menu, submenu
from src.core import config

app = FastAPI(
    title=config.PROJECT_NAME,
    description="Домашнее задание #3 YLab",
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
)


@app.get(
    path="/",
    summary="root",
    tags=["root"],
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def read_root():
    return {"Hello": "YLab"}


app.include_router(router=menu.router, prefix="/api/v1")
app.include_router(router=submenu.router, prefix="/api/v1/menus/{menu_id}")
app.include_router(
    router=dish.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
)
app.include_router(router=full_menu.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
