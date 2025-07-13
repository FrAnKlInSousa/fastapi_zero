from http import HTTPStatus

from fastapi_zero.schemas import UserPublic
from fastapi_zero.security import create_access_token


def test_root(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_hello_http(client):
    response = client.get('/hello')
    assert (
        response.text
        == """
    <!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Hello</title>
</head>
<body>
	<h1>Hello World!!!</h1>
</body>
</html>
"""
    )
    assert response.status_code == HTTPStatus.OK


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
            'username': 'Test',
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
            'email': 'test@test.com',
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
        'username': 'Test',
        'email': 'test@test.com',
        'id': 1,
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


def test_update_user_not_found(client, token, user):
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


def test_delete_other_user(client, token, user):
    new_user = client.post(
        '/users/',
        json={'username': 'new', 'email': 'new@new.com', 'password': '123'},
    )
    new_user_data = new_user.json()
    response = client.delete(
        f'/users/{new_user_data["id"]}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_updated_integrity_error(client, user, token):
    # inserindo usuário Fausto
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # alterando o user da fixture
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'newsecret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Usuário ou email já existe.'}


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    access_token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in access_token
    assert access_token['token_type'] == 'Bearer'


def test_get_token_email_error(client):
    data = {'password': '123'}
    access_token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token_user_error(client):
    data = {'sub': 'b@b.com'}
    access_token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_with_user_error(client):
    response = client.post(
        '/auth/token', data={'username': 'no-user@test.com', 'password': '123'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos.'}


def test_token_invalid_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'test@test.com', 'password': 'wrong_pass'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos.'}
