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
    assert user_db.username == 'test'
    assert user_db.email == 'test@test.com'
    assert user_db.password == 'secret'
    assert user_db.id == 1
    assert user_db.created_at == time
