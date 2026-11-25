import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db
from config import TestConfig


class SqliteTestConfig(TestConfig):
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }


@pytest.fixture
def client():
    app = create_app(SqliteTestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
