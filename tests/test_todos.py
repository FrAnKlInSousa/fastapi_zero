from http import HTTPStatus

import pytest

from fastapi_zero.models import Todo, TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            '/todos/',
            json={
                'title': 'test title',
                'description': 'test description',
                'state': 'draft',
            },
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            'id': 1,
            'title': 'test title',
            'description': 'test description',
            'state': 'draft',
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()
    response = client.get(
        '/todos/',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todo_pagination_should_return_2_todos(
    token, client, session, user
):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()
    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, token, client
):
    expected_todos = 5

    session.add_all(TodoFactory.create_batch(5, title='Test todo 1'))
    session.add_all(TodoFactory.create_batch(5))
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, description='desc test'))
    session.add_all(TodoFactory.create_batch(5, description='no match'))
    await session.commit()

    response = client.get(
        '/todos/?description=desc test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    token, session, client
):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, state=TodoState.draft))
    session.add_all(TodoFactory.create_batch(5, state=TodoState.done))
    await session.commit()

    response = client.get(
        '/todos/?state=draft', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo(make_todo, client, token):
    response = client.delete(
        f'/todos/{make_todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task deletada.'}


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/0', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task não encontrada.'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(client, token, other_user_todo):
    response = client.delete(
        f'/todos/{other_user_todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task não encontrada.'}


@pytest.mark.asyncio
async def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/0',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task não encontrada.'}


@pytest.mark.asyncio
async def test_patch_todo(token, client, mock_db_time, make_frozen_todo):
    with mock_db_time(model=Todo) as time:
        my_todo = await make_frozen_todo()
        response = client.patch(
            f'/todos/{my_todo.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={'title': 'updated title'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'title': 'updated title',
            'description': my_todo.description,
            'id': my_todo.id,
            'state': my_todo.state,
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }
