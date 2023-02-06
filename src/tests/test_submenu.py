import pytest
import pytest_asyncio
from fastapi import status

menu_id = 0
submenu_id = 0


class TestSubmenus:
    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def make_menu(self, test_app):
        test_menu_data = {"title": "Menu X", "description": "description X"}
        response = await test_app.post(
            "/api/v1/menus",
            json=test_menu_data,
        )
        global menu_id
        menu_id = response.json()["id"]
        yield
        await test_app.delete(f"/api/v1/menus/{menu_id}")

    @pytest.mark.asyncio
    async def test_get_submenus_empty(self, test_app):
        response = await test_app.get(f"/api/v1/menus/{menu_id}/submenus")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_create_submenu(self, test_app):
        test_submenu_data = {
            "title": "Submenu 1",
            "description": "Submenu description 1",
        }
        response = await test_app.post(
            f"api/v1/menus/{menu_id}/submenus",
            json=test_submenu_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() != []
        global submenu_id
        submenu_id = response.json()["id"]

    @pytest.mark.asyncio
    async def test_get_submenu_not_empty(self, test_app):
        test_submenu_data = {
            "title": "Submenu 1",
            "description": "Submenu description 1",
        }
        response = await test_app.get(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []
        assert response.json()["title"] == test_submenu_data["title"]
        assert response.json()["description"] == test_submenu_data["description"]

    @pytest.mark.asyncio
    async def test_get_submenu_by_id(self, test_app):
        global submenu_id
        response = await test_app.get(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": submenu_id,
            "title": "Submenu 1",
            "description": "Submenu description 1",
            "dishes_count": 0,
        }

    @pytest.mark.asyncio
    async def test_get_submenu_by_incorrect_id(self, test_app):
        response = await test_app.get(f"/api/v1/menus/{menu_id}/submenus/10000")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "submenu not found"}

    @pytest.mark.asyncio
    async def test_patch_submenu_by_id(self, test_app):
        test_updated_data = {
            "title": "Updated submenu 1",
            "description": "Updated description 1",
        }
        response = await test_app.patch(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
            json=test_updated_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == test_updated_data["title"]
        assert response.json()["description"] == test_updated_data["description"]

    @pytest.mark.asyncio
    async def test_patch_submenu_by_incorrect_id(self, test_app):
        test_updated_data = {
            "title": "Updated submenu 1",
            "description": "Updated description 1",
        }
        response = await test_app.patch(
            f"/api/v1/menus/{menu_id}/submenus/10000",
            json=test_updated_data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "submenu not found"}

    @pytest.mark.asyncio
    async def test_delete_submenu(self, test_app):
        global menu_id
        global submenu_id
        response = await test_app.delete(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "true",
            "message": "The submenu has been deleted",
        }

    @pytest.mark.asyncio
    async def test_delete_submenu_not_exist(self, test_app):
        response = await test_app.delete(f"/api/v1/menus/{menu_id}/submenus/10000")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "submenu not found"}
