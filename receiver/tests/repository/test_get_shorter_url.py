import pytest

from repository.shorter_urls import ShorterUrlsRepository


@pytest.mark.asyncio
async def test_get_shorter_url(session) -> None:
    shorter_urls_repository = ShorterUrlsRepository(session)
    short_url = "test"
    result = await shorter_urls_repository.get(short_url)
    assert result.short_url == short_url
