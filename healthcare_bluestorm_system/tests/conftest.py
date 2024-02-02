import pytest
from healthcare_bluestorm_system import app
from healthcare_bluestorm_system.app import create_app, minimal_app
from healthcare_bluestorm_system.ext.database import db
from healthcare_bluestorm_system.ext.commands import populate_db


@pytest.fixture(scope="session")
def min_app():
    app = minimal_app(FORCE_ENV_FOR_DYNACONF="backend_test")
    return app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="backend_test")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="session")
def users(app):
    with app.app_context():
        return populate_db()

@pytest.fixture
def client(app):
    return app.test_client()
