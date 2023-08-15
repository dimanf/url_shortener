from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from dto.visited_urls import VisitedUrlCreateDto
from models.visited_urls import VisitedUrls


class VisitedUrlsRepository:
    def __init__(self, db_engine: AsyncEngine):
        self.db_engine = db_engine

    async def create(self, visited_url: VisitedUrlCreateDto):
        async with self.db_engine.begin() as conn:
            record = await conn.execute(
                insert(VisitedUrls).values(**visited_url.model_dump()).returning(VisitedUrls)
            )

            return record
