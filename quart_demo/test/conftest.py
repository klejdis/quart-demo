import pytest
from quart import Quart
from quart.typing import TestClientProtocol

from quart_demo.app import create_app


@pytest.fixture(scope="session")
def app() -> Quart:
    return create_app()


@pytest.fixture()
def client(app: Quart) -> TestClientProtocol:
    return app.test_client()
