import logging
from typing import Union

from aiohttp import web
from aiohttp.abc import StreamResponse, Request
from asyncpg import Record
from pydantic import ValidationError
from dto.visited_urls import VisitedUrlCreateDto
from repository.shorter_urls import ShorterUrlsRepository
from repository.visited_urls import VisitedUrlsRepository

logging.basicConfig(
    format="%(asctime)s %(message)s",  # noqa
    datefmt="%d/%m/%Y %I:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


class ShorterUrlHandler:
    def __init__(
        self, shorter_urls_repo: ShorterUrlsRepository, visited_urls_repo: VisitedUrlsRepository
    ) -> None:
        self.shorter_urls_repo = shorter_urls_repo
        self.visited_urls_repo = visited_urls_repo

    async def __log_and_redirect(self, shorter_url: Union[Record, None]) -> StreamResponse:
        try:
            vu = VisitedUrlCreateDto.model_validate(
                {
                    "short_url": shorter_url.short_url,
                    "accn_id": shorter_url.data.get("accn_id"),  # noqa
                    "unsubscribe": shorter_url.data.get("unsubscribe"),
                }
            )
            await self.visited_urls_repo.create(vu)
        except ValidationError as e:
            logger.error(e.json())
            raise e

        return web.Response(status=302, headers={"location": shorter_url.original_url})

    async def get(self, request: Request) -> StreamResponse:
        short_url = request.match_info.get("short_url")
        if not short_url:
            raise Exception("You should provide a short url")
        su = await self.shorter_urls_repo.get(short_url)
        if not su:
            return web.Response(status=404)

        logger.info(f"Redirecting to: {su.original_url}")

        return await self.__log_and_redirect(su)
