import pytest
from fastapi import status
from httpx import AsyncClient

menu_id = 0


class TestMenu:
    @pytest.mark.asyncio
    async def test_get_menu_empty(self, test_app: AsyncClient):
        response = await test_app.get("/api/v1/menus")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_create_menu(self, test_app: AsyncClient):
        test_data = {"title": "Menu 1", "description": "Menu description 1"}
        response = await test_app.post(url="/api/v1/menus", json=test_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() != []
        global menu_id
        menu_id = response.json()["id"]

    @pytest.mark.asyncio
    async def test_get_menu_not_empty(self, test_app):
        response = await test_app.get("/api/v1/menus")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []

    @pytest.mark.asyncio
    async def test_get_menu_by_id(self, test_app):
        response = await test_app.get(f"/api/v1/menus/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": menu_id,
            "title": "Menu 1",
            "description": "Menu description 1",
            "submenus_count": 0,
            "dishes_count": 0,
        }

    @pytest.mark.asyncio
    async def test_get_menu_by_incorrect_id(self, test_app):
        response = await test_app.get("/api/v1/menus/100000")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "menu not found"}

    @pytest.mark.asyncio
    async def test_patch_menu_by_id(self, test_app):
        test_update_data = {
            "title": "Updated menu 1",
            "description": "Updated menu description 1",
        }
        response = await test_app.patch(
            f"/api/v1/menus/{menu_id}",
            json=test_update_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == test_update_data["title"]
        assert response.json()["description"] == test_update_data["description"]

    @pytest.mark.asyncio
    async def test_patch_menu_by_incorrect_id(self, test_app):
        test_update_data = {
            "title": "Updated menu 1",
            "description": "Updated menu description 1",
        }
        response = await test_app.patch(
            "/api/v1/menus/10000",
            json=test_update_data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "menu not found"}

    @pytest.mark.asyncio
    async def test_del_menu(self, test_app):
        response = await test_app.delete(f"/api/v1/menus/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "true",
            "message": "The menu has been deleted",
        }

    @pytest.mark.asyncio
    async def test_del_menu_not_exist(self, test_app):
        response = await test_app.delete("/api/v1/menus/10000")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "menu not found"}

    @pytest.mark.asyncio
    async def test_root(self, test_app):
        response = await test_app.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "YLab"}


#
