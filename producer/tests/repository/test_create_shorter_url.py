import pytest

from repository.repository import ShorterUrlsRepository
from tests.repository.mocks import shorter_url_create

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_save_shorter_url(session) -> None:
    repo = ShorterUrlsRepository(session)
    record = await repo.create(shorter_url_create)
    result = record.fetchone()._asdict()
    assert result.get("original_url") == shorter_url_create.original_url
    assert result.get("short_url") == shorter_url_create.short_url
    assert result.get("data").get("accn_id") == shorter_url_create.data.accn_id
    assert result.get("data").get("unsubscribe") == shorter_url_create.data.unsubscribe
    assert result.get("data").get("msg_id") == shorter_url_create.data.msg_id
