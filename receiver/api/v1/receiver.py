import logging
from aiohttp import web

from services.shorter_urls import ShorterUrlHandler

from repository.shorter_urls import ShorterUrlsRepository
from repository.visited_urls import VisitedUrlsRepository
from config.config import Config
from db.db import ProducerDatabase, ReceiverDatabase


def main():
    logging.basicConfig(
        format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
    )

    app = web.Application()
    pdb_conn = ProducerDatabase(
        dsn="postgresql+asyncpg://{username}:{password}@{db_host}/{db_name}".format(
            username=Config.POSTGRES_USER.get_env(),
            password=Config.POSTGRES_PASSWORD.get_env(),
            db_host=Config.POSTGRES_HOST.get_env(),
            db_name=Config.PRODUCER_DB_NAME.get_env(),
        )
    ).connect()
    rdb_conn = ReceiverDatabase(
        dsn="postgresql+asyncpg://{username}:{password}@{db_host}/{db_name}".format(
            username=Config.POSTGRES_USER.get_env(),
            password=Config.POSTGRES_PASSWORD.get_env(),
            db_host=Config.POSTGRES_HOST.get_env(),
            db_name=Config.RECEIVER_DB_NAME.get_env(),
        )
    ).connect()
    shorter_urls_repo = ShorterUrlsRepository(pdb_conn)
    visited_urls_repo = VisitedUrlsRepository(rdb_conn)
    handler = ShorterUrlHandler(shorter_urls_repo, visited_urls_repo)

    app.add_routes(
        [
            web.get("/{short_url}", handler.get),
        ]
    )

    web.run_app(
        app,
        host=Config.SERVER_HOST.get_env(),
        port=Config.SERVER_PORT.get_env(),
    )
