"""create location table"""
from alembic import op
import sqlalchemy as sa

revision = "f2ae49e845e3"
down_revision = "e87d20882edb"


def upgrade():
    op.create_table(
        "location",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.UnicodeText, nullable=False),
        sa.Column("abbreviation", sa.UnicodeText, nullable=False),
        sa.Column("address", sa.UnicodeText),
    )


def downgrade():
    op.drop_table("location")
