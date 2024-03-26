from typing import Any

from quart_demo.clients.base_client import BaseClient


class JsonPlaceholder(BaseClient):
    async def get_fake_posts(self) -> Any:
        res = await self._client.get(f"{self.server_url}/posts")
        return res.json()
