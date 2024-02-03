import asyncio
import os
from asyncio import AbstractEventLoop
from pathlib import Path
from typing import AsyncGenerator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from quart import Quart
from quart.typing import TestClientProtocol
from sqlalchemy import delete

from quart_demo.app import create_app
from quart_demo.database.connection import async_session
from quart_demo.models.models import Posts


@pytest.fixture(scope="session")
def app() -> Quart:
    return create_app()


@pytest.fixture()
def client(app: Quart) -> TestClientProtocol:
    return app.test_client()


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """Redefinition of pytest's event loop fixture to change the scope to session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def alembic_config() -> Config:
    root_directory = Path(__file__).parent.parent.parent
    alembic_directory = os.path.join(root_directory, "migrations")
    ini_path = os.path.join(root_directory, "alembic.ini")
    alembic_cfg = Config(ini_path)
    alembic_cfg.set_main_option("script_location", alembic_directory)
    return alembic_cfg


@pytest.fixture(scope="session")
async def migrated_database(app: Quart, alembic_config: Config) -> AsyncGenerator[None, None]:
    command.upgrade(alembic_config, "head")
    yield
    command.downgrade(alembic_config, "base")


async def _delete_database_entries(raise_exceptions: bool = True) -> None:
    async with async_session.begin() as session:
        for entity in [
            Posts,
        ]:
            try:
                await session.execute(delete(entity))
            except Exception as e:
                if raise_exceptions:
                    raise e


@pytest.fixture()
async def refresh_database(migrated_database: None) -> AsyncGenerator[None, None]:
    await _delete_database_entries()
    yield
    await _delete_database_entries()
