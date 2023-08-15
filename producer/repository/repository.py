from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from models.shorter_urls import ShorterUrls

from dto.message import ShorterUrlCreate


class ShorterUrlsRepository:
    def __init__(self, db_session: async_sessionmaker[AsyncSession]):
        self.db_session = db_session

    async def create(self, shorter_url: ShorterUrlCreate):
        async with self.db_session() as session:
            result = await session.execute(
                insert(ShorterUrls).values(**shorter_url.model_dump()).returning(ShorterUrls)
            )
            await session.commit()
            return result
