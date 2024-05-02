"""Create course table"""
from alembic import op
import sqlalchemy as sa


revision = "39d766b657c0"
down_revision = "302342f805df"


def upgrade():
    op.create_table(
        "course",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("location.id"), nullable=True),
        sa.Column("day", sa.UnicodeText(), nullable=True),
        sa.Column("time", sa.UnicodeText(), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("level.id"), nullable=True),
        sa.Column("code", sa.UnicodeText(), nullable=False),
        sa.Column("memeo", sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("course")
