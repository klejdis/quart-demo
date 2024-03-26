from quart_demo.clients.json_placeholder import JsonPlaceholder
from quart_demo.config import settings


async def test_json_placeholder() -> None:
    JsonPlaceholder(server_url=settings.json_placeholder.server_url).init_connection()

    jp = JsonPlaceholder.get_instance()
    jp = await jp.get_fake_posts()

    assert jp is not None
