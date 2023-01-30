import json

from fastapi import status

menu_id = 0


def test_root(test_app):
    response = test_app.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'Hello': 'YLab'}


def test_get_menu_empty(test_app):
    response = test_app.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_menu(test_app):
    test_data = {'title': 'Menu 1', 'description': 'Menu description 1'}
    response = test_app.post('api/v1/menus', content=json.dumps(test_data))
    print('=>', response)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != []
    global menu_id
    menu_id = response.json()['id']


def test_get_menu_not_empty(test_app):
    response = test_app.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []


def test_get_menu_by_id(test_app):
    response = test_app.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': menu_id, 'title': 'Menu 1', 'description': 'Menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }


def test_get_menu_by_incorrect_id(test_app):
    response = test_app.get('/api/v1/menus/100000')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'menu not found'}


def test_patch_menu_by_id(test_app):
    test_update_data = {
        'title': 'Updated menu 1',
        'description': 'Updated menu description 1',
    }
    response = test_app.patch(
        f'/api/v1/menus/{menu_id}', content=json.dumps(test_update_data),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == test_update_data['title']
    assert response.json()['description'] == test_update_data['description']


def test_patch_menu_by_incorrect_id(test_app):
    test_update_data = {
        'title': 'Updated menu 1',
        'description': 'Updated menu description 1',
    }
    response = test_app.patch(
        '/api/v1/menus/10000',
        content=json.dumps(test_update_data),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'menu not found'}


def test_del_menu(test_app):
    response = test_app.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'status': 'true',
        'message': 'The menu has been deleted',
    }


def test_del_menu_not_exist(test_app):
    response = test_app.delete('/api/v1/menus/10000')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'menu not found'}
