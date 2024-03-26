from typing import Any

import httpx
from quart import Quart

from quart_demo.utilities import SingletonMeta


class BaseClient(metaclass=SingletonMeta):
    _client: httpx.AsyncClient

    def __init__(self, server_url: str):
        self.server_url = server_url

    def init_app(self, app: Quart) -> None:
        @app.before_serving
        async def before_serving() -> None:
            self.init_connection()

        @app.after_serving
        async def after_serving() -> None:
            await self._client.aclose()

    def init_connection(self) -> None:
        # for given config init the _client with httpx.AsyncClient
        # some extra config can be added for transport limit etc
        self._client = httpx.AsyncClient(base_url=self.server_url)

    @classmethod
    def get_instance(cls) -> Any:
        if cls not in cls._instances:
            raise Exception("Not Initialized")
        return cls._instances[cls]
