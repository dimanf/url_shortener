import pytest


@pytest.mark.asyncio
async def test_redirect_original_url(web_client) -> None:
    resp = await web_client.get("/test-url")
    assert resp.status == 304
