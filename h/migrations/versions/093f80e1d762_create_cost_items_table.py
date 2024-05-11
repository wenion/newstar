"""Create cost items table"""
from alembic import op

import sqlalchemy as sa


revision = "093f80e1d762"
down_revision = "a853a150b2ed"


def upgrade():
    op.create_table(
        "cost_item",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),

        sa.Column("number", sa.UnicodeText(), nullable=True),
        sa.Column("name", sa.UnicodeText(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("gst_included", sa.Float(), nullable=True),
        sa.Column("comments", sa.UnicodeText(), nullable=True),

        sa.Column("level_id", sa.Integer(), nullable=True),
        sa.Column("term_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(["term_id"], ["term.id"]),
        sa.ForeignKeyConstraint(["level_id"], ["level.id"]),
    )
    op.create_index(op.f("uq__cost_item__number"), "cost_item", ["number"], unique=True)


def downgrade():
    op.drop_index(op.f("uq__cost_item__number"), table_name="cost_item")
    op.drop_table("cost_item")
