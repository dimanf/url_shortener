import pytest
from asyncpg import UniqueViolationError

from repository.repository import ShorterUrlsRepository
from services.handler import ShorterUrlHandler
from tests.services.mocks import shorter_url_dto

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_save_shorter_url(session) -> None:
    repo = ShorterUrlsRepository(session)
    handler = ShorterUrlHandler(repo)
    record = await handler.save(shorter_url_dto.model_dump_json())
    result = record.fetchone()._asdict()
    assert result.get("original_url") == shorter_url_dto.url


@pytest.mark.xfail(raises=UniqueViolationError)
async def test_save_shorter_url_rises_unique_error(session) -> None:
    repo = ShorterUrlsRepository(session)
    handler = ShorterUrlHandler(repo)
    record = await handler.save(shorter_url_dto.model_dump_json())
    result = record.fetchone()._asdict()
    assert result.get("original_url") == shorter_url_dto.url
