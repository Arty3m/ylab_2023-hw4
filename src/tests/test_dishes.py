import json

import pytest
from fastapi import status

menu_id = 0
submenu_id = 0
dish_id = 0


class TestDishes:
    @pytest.fixture(scope='class', autouse=True)
    def make_menu_and_submenu(self, test_app):
        test_menu_data = {'title': 'Menu X', 'description': 'description X'}
        response = test_app.post(
            '/api/v1/menus', content=json.dumps(test_menu_data),
        )
        global menu_id
        menu_id = response.json()['id']
        test_submenu_data = {
            'title': 'Submenu 1',
            'description': 'Submenu description 1',
        }
        response = test_app.post(
            f'api/v1/menus/{menu_id}/submenus', content=json.dumps(test_submenu_data),
        )
        global submenu_id
        submenu_id = response.json()['id']
        yield
        test_app.delete(f'/api/v1/menus/{menu_id}')

    def test_get_dishes_empty(self, test_app):
        response = test_app.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_dishes(self, test_app):
        test_dish = {
            'title': 'Dish 1',
            'description': 'Dish description 1', 'price': '12.555',
        }
        response = test_app.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
            content=json.dumps(test_dish),
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() != []
        assert response.json()['title'] == test_dish['title']
        assert response.json()['description'] == test_dish['description']
        # check around price
        assert response.json()['price'] == '12.55'
        global dish_id
        dish_id = response.json()['id']

    def test_get_dishes_not_empty(self, test_app):
        response = test_app.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []

    def test_get_dish_by_id(self, test_app):
        response = test_app.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': dish_id, 'title': 'Dish 1', 'description': 'Dish description 1',
            'price': '12.55',
        }

    def test_get_dish_by_incorrect_id(self, test_app):
        response = test_app.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/10000',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'dish not found'}

    def test_patch_dish_by_id(self, test_app):
        test_updated_dish = {
            'title': 'Updated dish 1',
            'description': 'Updated dish description 1', 'price': '333',
        }
        response = test_app.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            content=json.dumps(test_updated_dish),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == test_updated_dish['title']
        assert response.json()[
            'description'
        ] == test_updated_dish['description']
        assert response.json()['price'] == test_updated_dish['price']

    def test_patch_dish_by_incorrect_id(self, test_app):
        test_updated_dish = {
            'title': 'Updated dish 1',
            'description': 'Updated dish description 1', 'price': '333',
        }
        response = test_app.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/10000',
            content=json.dumps(test_updated_dish),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'dish not found'}

    def test_delete_dish(self, test_app):
        response = test_app.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'status': 'true',
            'message': 'The dish has been deleted',
        }

    def test_delete_dish_not_exist(self, test_app):
        response = test_app.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'dish not found'}
