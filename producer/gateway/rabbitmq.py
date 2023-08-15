import logging
from typing import Callable, Awaitable, Any

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel


logging.basicConfig(
    format="%(asctime)s %(message)s",  # noqa
    datefmt="%d/%m/%Y %I:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


class RabbitMQ:
    def __init__(self, queue, host, routing_key, username, password, exchange=""):
        self.username = username
        self.password = password
        self.host = host
        self.queue = queue
        self.routing_key = routing_key
        self.exchange = exchange

    async def connect(self) -> AbstractConnection:
        conn: AbstractConnection = await aio_pika.connect(
            login=self.username,
            password=self.password,
            host=self.host,
        )
        return conn

    async def consume(self, callback: Callable[[Any], Awaitable[Any]]) -> None:
        conn = await self.connect()
        channel: AbstractChannel = await conn.channel()
        exchange = await channel.declare_exchange(
            "url_shortener_receiver",
            auto_delete=True,
        )
        queue = await channel.declare_queue(name=self.queue)
        await queue.bind(exchange)
        await queue.consume(callback)

        logger.info("Message consuming started")
