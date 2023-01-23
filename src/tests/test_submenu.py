import pytest
import json
from fastapi import status

menu_id = 0
submenu_id = 0


class TestSubmenus:
    @pytest.fixture(scope='class', autouse=True)
    def make_menu(self, test_app):
        test_menu_data = {"title": "Menu X", "description": "description X"}
        response = test_app.post('/api/v1/menus', content=json.dumps(test_menu_data))
        global menu_id
        menu_id = response.json()['id']
        yield
        test_app.delete(f'/api/v1/menus/{menu_id}')

    def test_get_submenus_empty(self, test_app):
        response = test_app.get(f'/api/v1/menus/{menu_id}/submenus')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_submenu(self, test_app):
        test_submenu_data = {"title": "Submenu 1", "description": "Submenu description 1"}
        response = test_app.post(f'api/v1/menus/{menu_id}/submenus', content=json.dumps(test_submenu_data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() != []
        global submenu_id
        submenu_id = response.json()['id']

    def test_get_submenu_not_empty(self, test_app):
        test_submenu_data = {"title": "Submenu 1", "description": "Submenu description 1"}
        response = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []
        assert response.json()['title'] == test_submenu_data['title']
        assert response.json()['description'] == test_submenu_data['description']

    def test_get_submenu_by_id(self, test_app):
        global submenu_id
        response = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": submenu_id, "title": "Submenu 1", "description": "Submenu description 1",
                                   "dishes_count": 0}

    def test_get_submenu_by_incorrect_id(self, test_app):
        response = test_app.get(f'/api/v1/menus/{menu_id}/submenus/10000')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'submenu not found'}

    def test_patch_submenu_by_id(self, test_app):
        test_updated_data = {'title': 'Updated submenu 1', 'description': 'Updated description 1'}
        response = test_app.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
                                  content=json.dumps(test_updated_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == test_updated_data['title']
        assert response.json()['description'] == test_updated_data['description']

    def test_patch_submenu_by_incorrect_id(self, test_app):
        test_updated_data = {'title': 'Updated submenu 1', 'description': 'Updated description 1'}
        response = test_app.patch(f'/api/v1/menus/{menu_id}/submenus/10000',
                                  content=json.dumps(test_updated_data))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'submenu not found'}

    def test_delete_submenu(self, test_app):
        global menu_id
        global submenu_id
        response = test_app.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'status': 'true', 'message': 'The submenu has been deleted'}

    def test_delete_submenu_not_exist(self, test_app):
        response = test_app.delete(f'/api/v1/menus/{menu_id}/submenus/10000')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'submenu not found'}
