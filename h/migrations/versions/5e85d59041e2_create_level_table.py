"""Create level table"""
import sqlalchemy as sa
from alembic import op


revision = "5e85d59041e2"
down_revision = "f2ae49e845e3"


def upgrade():
    op.create_table(
        "level",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.UnicodeText(), nullable=False),
        sa.Column("abbreviation", sa.UnicodeText(), nullable=False),
        sa.Column("start_age", sa.UnicodeText(), nullable=True),
        sa.Column("end_age", sa.UnicodeText(), nullable=True),
    )


def downgrade():
    op.drop_table("level")
