from flask.testing import FlaskClient
import pytest

from app import app


@pytest.fixture(scope="module")
def test_client():
    flask_app = app

    flask_app.testing = True
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
