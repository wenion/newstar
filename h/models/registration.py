import sqlalchemy as sa

from h.db import Base, mixins


class RegistrationTermOption(Base, mixins.Timestamps):
    __tablename__ = "registration_term_option"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), nullable=False)

    chinese = sa.Column("chinese", sa.UnicodeText(), nullable=False)

    def __repr__(self):
        return f"<Registration Term Option: {self.name}>"


class RegistrationSourceOption(Base, mixins.Timestamps):
    __tablename__ = "registration_source_option"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), nullable=False)

    chinese = sa.Column("chinese", sa.UnicodeText(), nullable=False)

    def __repr__(self):
        return f"<Registration Source Option: {self.name}>"
