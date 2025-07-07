from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_hello_http():
    client = TestClient(app)
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
