from typing import Union

from asyncpg import Record
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.shorter_urls import ShorterUrls


class ShorterUrlsRepository:
    def __init__(self, db_session: async_sessionmaker[AsyncSession]):
        self.db_session = db_session

    async def get(self, short_url: str) -> Union[Record, None]:
        async with self.db_session() as session:
            result = await session.execute(
                select(ShorterUrls).where(ShorterUrls.c.short_url == short_url)
            )
            await session.commit()
            return result.first()
