"""empty message

Revision ID: ddf6a86b4108
Revises: 
Create Date: 2023-08-14 17:47:06.443021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ddf6a86b4108"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "visited_urls",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("short_url", sa.Text, nullable=False, index=True),
        sa.Column("accn_id", sa.Text, nullable=False),
        sa.Column("unsubscribe", sa.Boolean, nullable=False),
        sa.Column("created", sa.DateTime, nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("visited_urls")
