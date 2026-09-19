"""
Pytest fixtures - har test ke liye fresh in-memory DB + Flask test client.
"""
import pytest

from app import create_app
from app.config import TestConfig
from app.models import db as _db


@pytest.fixture(scope="function")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    return _db


@pytest.fixture
def auth_client(client):
    """Login karke wapas karta hai - protected pages test karne ke liye."""
    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
    return client
