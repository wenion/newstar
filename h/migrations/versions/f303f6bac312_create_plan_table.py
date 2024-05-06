"""Create plan table"""
from alembic import op
import sqlalchemy as sa


revision = "f303f6bac312"
down_revision = "39d766b657c0"


def upgrade():
    op.create_table(
        "plan",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.UnicodeText(), nullable=False),
        sa.Column("code_id", sa.Integer(), sa.ForeignKey("course.id"), nullable=False),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("location.id"), nullable=False),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("level.id"), nullable=False),
        sa.Column("term_id", sa.Integer(), sa.ForeignKey("term.id"), nullable=False),
        sa.Column("start_time", sa.DateTime, nullable=False),
        sa.Column("end_time", sa.DateTime, nullable=False),
        sa.Column("memeo", sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("plan")
