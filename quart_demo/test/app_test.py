import pytest
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_health_endpoint(client: QuartClient) -> None:
    response = await client.get("/health-check")
    response_data = await response.get_data(as_text=True)

    assert response_data == "Healthy as a horse!"
