import pytest

from repository.visited_urls import VisitedUrlsRepository
from tests.repository.mocks import visited_url_create


@pytest.mark.asyncio
async def test_create_visited_url(pr_engine, session) -> None:
    visited_urls_repo = VisitedUrlsRepository(session)
    record = visited_urls_repo.create(visited_url_create)
    result = record.fetchone()._asdict()
    assert result.get("short_url") == visited_url_create.short_url
    assert result.get("accn_id") == visited_url_create.accn_id  # noqa
    assert result.get("unsubscribe") == visited_url_create.unsubscribe
