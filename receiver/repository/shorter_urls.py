from typing import Union

from asyncpg import Record
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from models.shorter_urls import ShorterUrls


class ShorterUrlsRepository:
    def __init__(self, db_engine: AsyncEngine):
        self.db_engine = db_engine

    async def get(self, short_url: str) -> Union[Record, None]:
        async with self.db_engine.begin() as conn:
            result = await conn.execute(
                select(ShorterUrls).where(ShorterUrls.c.short_url == short_url)
            )
            return result.first()
