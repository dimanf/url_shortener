import pytest

from repository.repository import ShorterUrlsRepository
from services.handler import ShorterUrlHandler


@pytest.mark.parametrize(
    "length_expected",
    [12, 8, 6],
)
def test_generate_shorten_url(session, length_expected) -> None:
    repo = ShorterUrlsRepository(session)
    handler = ShorterUrlHandler(repo)
    assert len(handler.generate_shorten_url(length=length_expected)) == length_expected
