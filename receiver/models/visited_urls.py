from sqlalchemy import Table, Column, Integer, Text, Boolean, DateTime, text

from models.base_metadata import metadata

VisitedUrls = Table(
    "visited_urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("short_url", Text(), nullable=False, index=True),
    Column("accn_id", Text(), nullable=False),  # noqa
    Column("unsubscribe", Boolean(), nullable=False),
    Column("created", DateTime, nullable=False, server_default=text("now()")),
)
