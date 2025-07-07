from http import HTTPStatus


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
