import pytest
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = orm.declarative_base()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine("postgresql+asyncpg://test:test@db:5432/test_url_shortener")
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
