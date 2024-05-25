"""remove_registration_from_profile"""
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

import sqlalchemy as sa


revision = "0c3a8c7d097f"
down_revision = "093f80e1d762"

Base = declarative_base()
Session = orm.sessionmaker()


class Registration(Base):
    __tablename__ = "registration"
    id = sa.Column("id", sa.Integer, primary_key=True)


class Profile(Base):
    __tablename__ = "profile"
    id = sa.Column("id", sa.Integer, primary_key=True)
    registration_id = sa.Column(sa.Integer, sa.ForeignKey("registration.id"), nullable=True)
    registration = sa.orm.relationship("Registration", backref="profile")


class ProfileRegistration(Base):
    __tablename__ = "profile_registration"
    id = sa.Column("id", sa.Integer, autoincrement=True, primary_key=True)
    profile_id = sa.Column("profile_id", sa.Integer(), nullable=True)
    registration_id = sa.Column("registration_id", sa.Integer(), nullable=True)


def upgrade():
    op.create_table(
        "profile_registration",
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("created", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated", sa.DateTime, server_default=sa.func.now(), nullable=False),
        
        sa.Column("profile_id", sa.Integer(), nullable=True),
        sa.Column("registration_id", sa.Integer(), nullable=True),
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    for profile in session.query(Profile):
        if profile.registration_id:
            pr = ProfileRegistration(profile_id=profile.id, registration_id=profile.registration_id)
            session.add(pr)

    session.commit()

    op.drop_column("profile", "registration_id")


def downgrade():
    op.add_column("profile", sa.Column("registration_id", sa.Integer, sa.ForeignKey("registration.id"), nullable=True))

    profile_table = sa.table(
        "profile",
        sa.Column("id", sa.Integer),
        sa.Column("registration_id", sa.ForeignKey("registration.id"), nullable=True),
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    for pr in session.query(ProfileRegistration):
        op.execute(
            profile_table.update()
            .where(profile_table.c.id == pr.profile_id)
            .values(registration_id = pr.registration_id)
        )

    op.drop_table("profile_registration")