from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/4',
        json={'username': 'frank', 'email': 'a@a.com', 'password': 'aaa'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado.'}
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_not_found(client):
    response = client.delete('/users/33')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updated_integrity_error(client, user):
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
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'newsecret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Usuário ou email já existe.'}
