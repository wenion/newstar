"""Create profile table"""
from alembic import op
import sqlalchemy as sa


revision = "a853a150b2ed"
down_revision = "bafd87159e12"


def upgrade():
    op.create_table(
        "profile",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        
        sa.Column("number", sa.UnicodeText(), nullable=True),
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
        sa.Column("memeo", sa.UnicodeText(), nullable=True),

        sa.Column("registration_id", sa.Integer(), nullable=True),
        sa.Column("referer_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["referer_id"], ["profile.id"]),
        sa.ForeignKeyConstraint(["registration_id"], ["registration.id"]),
    )
    op.create_index(op.f("uq__profile__number"), "profile", ["number"], unique=True)


def downgrade():
    op.drop_index(op.f("uq__profile__number"), table_name="profile")
    op.drop_table("profile")
