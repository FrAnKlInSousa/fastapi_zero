from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_create_user(client):
    user = {
        'username': 'franklin',
        'email': 'frank@gmail.com',
        'password': '12344',
    }

    response = client.post(
        '/users/',
        json=user,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'franklin',
        'email': 'frank@gmail.com',
        'id': 1,
    }


def test_create_user_with_existing_username(user, client):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'email@email.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_with_existing_email(user, client):
    response = client.post(
        '/users/',
        json={
            'username': 'frank',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_not_found(client):
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'updated',
            'email': 'new@gmail.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'updated',
        'email': 'new@gmail.com',
        'id': 1,
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/4',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'frank', 'email': 'a@a.com', 'password': 'aaa'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado.'}
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_wrong_user(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissão.'}


def test_updated_integrity_error(client, user, other_user, token):
    # alterando o user da fixture
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'bob@example.com',
            'password': 'newsecret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Usuário ou email já existe.'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissão.'}
