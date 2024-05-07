"""Create registration options"""
import sqlalchemy as sa
from alembic import op


revision = "858f7b447068"
down_revision = "f303f6bac312"


def upgrade():
    op.create_table(
        "registration_term_option",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.UnicodeText(), nullable=False),
        sa.Column("chinese", sa.UnicodeText(), nullable=False),
    )

    op.create_table(
        "registration_source_option",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.UnicodeText(), nullable=False),
        sa.Column("chinese", sa.UnicodeText(), nullable=False),
    )


def downgrade():
    op.drop_table("registration_source_option")
    op.drop_table("registration_term_option")
