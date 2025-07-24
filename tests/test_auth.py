from http import HTTPStatus

from fastapi_zero.security import create_access_token


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
        data={'username': user.email, 'password': 'wrong_pass'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos.'}
