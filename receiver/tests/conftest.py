import pytest
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from dto.visited_urls import VisitedUrlCreateDto
from repository.visited_urls import VisitedUrlsRepository

Base = orm.declarative_base()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/receiver")
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
def pr_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/url_shortener"
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture()
async def web_client(loop, aiohttp_client, pr_engine, session):
    visited_urls_repo = VisitedUrlsRepository(session)

    vu = VisitedUrlCreateDto(
        short_url="test",
        accn_id="accn_id",  # noqa
        unsubscribe=False,
    )
    await visited_urls_repo.create(vu)
