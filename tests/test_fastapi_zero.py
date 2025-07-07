from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK
