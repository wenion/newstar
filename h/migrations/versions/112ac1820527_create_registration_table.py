"""Create registration table"""
import enum

import sqlalchemy as sa
from alembic import op


revision = "112ac1820527"
down_revision = "858f7b447068"


def upgrade():
    op.create_table(
        "registration",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        
        sa.Column("first_name", sa.UnicodeText(), nullable=True),
        sa.Column("last_name", sa.UnicodeText(), nullable=True),
        sa.Column("date_of_birth", sa.DateTime(), nullable=True),
        sa.Column("gender", sa.UnicodeText(), nullable=True),

        sa.Column("wechat", sa.UnicodeText(), nullable=True),
        sa.Column("email", sa.UnicodeText(), nullable=True),
        sa.Column("phone", sa.UnicodeText(), nullable=True),
        sa.Column("first_emergency_contact", sa.UnicodeText(), nullable=True),
        sa.Column("second_emergency_contact", sa.UnicodeText(), nullable=True),
        sa.Column("emergency_contact", sa.UnicodeText()),

        sa.Column("level_id", sa.Integer(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("code_id", sa.Integer(), nullable=True),
        sa.Column("term_id", sa.Integer(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),

        sa.Column("referer", sa.UnicodeText(), nullable=True),
        sa.Column("memeo", sa.UnicodeText(), nullable=True),
        sa.Column("privacy_accepted", sa.DateTime, nullable=True),

        sa.ForeignKeyConstraint(["source_id"], ["registration_source_option.id"]),
        sa.ForeignKeyConstraint(["term_id"], ["registration_term_option.id"]),
        sa.ForeignKeyConstraint(["code_id"], ["course.id"]),
        sa.ForeignKeyConstraint(["location_id"], ["location.id"]),
        sa.ForeignKeyConstraint(["level_id"], ["level.id"]),
    )


def downgrade():
    op.drop_table("registration")
