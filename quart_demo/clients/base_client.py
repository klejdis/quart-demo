from typing import TypeVar

import httpx

from quart_demo.config import Quart
from quart_demo.utilities import SingletonMeta


class BaseClient(metaclass=SingletonMeta):
    _client: httpx.AsyncClient

    def __init__(self, server_url: str):
        self.server_url = server_url

    def init_app(self, app: Quart):
        @app.before_serving
        async def before_serving() -> None:
            self.init_connection()

        @app.after_serving
        async def after_serving() -> None:
            await self._client.aclose()

    def init_connection(self):
        # for given config init the _client with httpx.AsyncClient
        # some extra config can be added for transport limit etc
        self._client = httpx.AsyncClient(base_url=self.server_url)

    @classmethod
    def get_instance(cls):
        if cls not in cls._instances:
            raise Exception("Not Initialized")
        return cls._instances[cls]
