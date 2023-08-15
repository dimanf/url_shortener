from sqlalchemy import Table, Column, Integer, Text, JSON, DateTime, text, UniqueConstraint

from models.base_metadata import metadata

ShorterUrls = Table(
    "shorter_urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("msg_id", Text(), nullable=False, index=True),
    Column("original_url", Text(), nullable=False),
    Column("short_url", Text(), nullable=False, index=True),
    Column("data", JSON, nullable=False),
    Column("created", DateTime, nullable=False, server_default=text("now()")),
    UniqueConstraint("original_url", name="original_url_short_url"),
)
