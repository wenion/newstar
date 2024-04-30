"""Create term table"""
import sqlalchemy as sa
from alembic import op


revision = "302342f805df"
down_revision = "5e85d59041e2"


def upgrade():
    op.create_table(
        "term",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.UnicodeText(), server_default="Term", nullable=False),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("year", sa.Integer, nullable=False, index=True),
        sa.Column("start_date", sa.DateTime, nullable=False),
        sa.Column("end_date", sa.DateTime, nullable=False),
        sa.Column("number_of_weeks", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("term")
