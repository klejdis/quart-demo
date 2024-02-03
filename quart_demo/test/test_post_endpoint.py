import pytest
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_post_create(client: QuartClient, refresh_database: None) -> None:
    response = await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    await response.get_data(as_text=True)

    assert response.status_code == 200
