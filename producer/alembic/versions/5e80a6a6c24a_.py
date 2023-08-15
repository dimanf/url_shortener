"""empty message

Revision ID: 5e80a6a6c24a
Revises: 
Create Date: 2023-08-13 20:45:39.139517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e80a6a6c24a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shorter_urls",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("msg_id", sa.Text, nullable=False, index=True),
        sa.Column("original_url", sa.Text, nullable=False),
        sa.Column("short_url", sa.Text, nullable=False, index=True),
        sa.Column("data", sa.JSON, nullable=False),
        sa.Column("created", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("original_url", name="original_url_idx"),
    )


def downgrade() -> None:
    op.drop_table("shorter_urls")
