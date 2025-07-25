from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.exc import DataError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret'
        )
        session.add(new_user)
        await session.commit()

        user_db = await session.scalar(
            select(User).where(User.username == 'test')
        )

    assert asdict(user_db) == {
        'id': 1,
        'username': 'test',
        'password': 'secret',
        'email': 'test@test.com',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo_error(session, user):
    todo = Todo(
        title='title', description='desc', state='error', user_id=user.id
    )
    session.add(todo)
    with pytest.raises(DataError):
        await session.commit()

    with pytest.raises(PendingRollbackError):
        await session.scalar(select(Todo))
