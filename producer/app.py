import asyncio
import logging

from dotenv import load_dotenv

from config.config import Config
from db.db import Database
from gateway.rabbitmq import RabbitMQ
from repository.repository import ShorterUrlsRepository
from services.handler import ShorterUrlHandler

logging.basicConfig(
    format="%(asctime)s %(message)s",  # noqa
    datefmt="%d/%m/%Y %I:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


if __name__ == "__main__":
    load_dotenv()
    loop = asyncio.get_event_loop()

    db_conn = Database(
        dsn="postgresql+asyncpg://{username}:{password}@{db_host}/{db_name}".format(
            username=Config.POSTGRES_USER.get_env(),
            password=Config.POSTGRES_PASSWORD.get_env(),
            db_host=Config.POSTGRES_HOST.get_env(),
            db_name=Config.POSTGRES_DB.get_env(),
        )
    ).connect()
    repo = ShorterUrlsRepository(db_conn)
    shorter_url_handler = ShorterUrlHandler(repo)
    rmq = RabbitMQ(
        username=Config.RABBITMQ_USERNAME.get_env(),
        password=Config.RABBITMQ_PASSWORD.get_env(),
        host=Config.RABBITMQ_HOST.get_env(),
        queue=Config.RABBITMQ_QUEUE.get_env(),
        routing_key=Config.RABBITMQ_ROUTING_KEY.get_env(),
        exchange=Config.RABBITMQ_EXCHANGE.get_env(),
    )
    connection = loop.run_until_complete(rmq.consume(shorter_url_handler.create))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
