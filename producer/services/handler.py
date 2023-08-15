import logging
import random
import string
from typing import Any

import aio_pika
from pydantic import ValidationError

from dto.message import ShorterUrlDto, ShorterUrlCreate
from repository.repository import ShorterUrlsRepository


logging.basicConfig(
    format="%(asctime)s %(message)s",  # noqa
    datefmt="%d/%m/%Y %I:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


class ShorterUrlHandler:
    def __init__(self, repo: ShorterUrlsRepository) -> None:
        self.repo = repo

    @staticmethod
    def generate_shorten_url(length=12):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    async def save(self, body) -> Any:
        try:
            message = ShorterUrlDto.model_validate_json(body)
            shorter_url = await self.repo.create(
                ShorterUrlCreate(
                    msg_id=message.data.msg_id,
                    original_url=message.url,
                    short_url=self.generate_shorten_url(),
                    data=message.data,
                )
            )
            return shorter_url
        except ValidationError as e:
            logger.error(e.json())
            raise e

    async def create(self, msg: aio_pika.IncomingMessage) -> None:
        async with msg.process():
            logger.info("Process started")
            await self.save(msg.body.decode())
