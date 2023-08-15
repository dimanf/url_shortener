from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from models.shorter_urls import ShorterUrls

from dto.message import ShorterUrlCreate


class ShorterUrlsRepository:
    def __init__(self, db_engine: AsyncEngine):
        self.db_engine = db_engine

    async def create(self, shorter_url: ShorterUrlCreate):
        async with self.db_engine.begin() as conn:
            record = await conn.execute(
                insert(ShorterUrls).values(**shorter_url.model_dump()).returning(ShorterUrls)
            )
            return record
