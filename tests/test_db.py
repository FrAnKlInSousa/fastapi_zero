from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(username='test', email='test@test.com', password='secret')
        session.add(user)
        session.commit()

        user_db = session.scalar(
            select(User).where(User.username == user.username)
        )

    assert asdict(user_db) == {
        'id': 1,
        'username': 'test',
        'password': 'secret',
        'email': 'test@test.com',
        'created_at': time,
        'updated_at': time,
    }
