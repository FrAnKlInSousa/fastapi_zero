from contextlib import contextmanager
from datetime import datetime

import factory.fuzzy
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, TodoState, User, table_registry
from fastapi_zero.security import get_password_hash
from fastapi_zero.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'secret'
    new_user = UserFactory(password=get_password_hash(password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    new_user.clean_password = password
    return new_user


@pytest_asyncio.fixture
async def other_user(session: AsyncSession):
    password = 'secret'
    new_user = UserFactory(password=get_password_hash(password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    new_user.clean_password = password
    return new_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()


@pytest_asyncio.fixture
def make_frozen_todo(user, session):
    async def _make():
        todo = TodoFactory(user_id=user.id)
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo

    return _make


@pytest_asyncio.fixture
async def make_todo(session, user):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


@pytest_asyncio.fixture
async def other_user_todo(other_user, session):
    my_todo = TodoFactory(user_id=other_user.id)
    session.add(my_todo)
    await session.commit()
    return my_todo


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}#secret')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1
