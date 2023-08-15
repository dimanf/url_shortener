from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from dto.visited_urls import VisitedUrlCreateDto
from models.visited_urls import VisitedUrls


class VisitedUrlsRepository:
    def __init__(self, db_session: async_sessionmaker[AsyncSession]):
        self.db_session = db_session

    async def create(self, visited_url: VisitedUrlCreateDto):
        async with self.db_session() as session:
            record = await session.execute(
                insert(VisitedUrls).values(**visited_url.model_dump()).returning(VisitedUrls)
            )
            await session.commit()
            return record
