import sqlalchemy as sa

from h.db import Base, mixins


class Location(Base, mixins.Timestamps):
    __tablename__ = "location"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), nullable=False)

    abbreviation = sa.Column("abbreviation", sa.UnicodeText(), nullable=False)

    address = sa.Column(sa.UnicodeText())

    def __repr__(self):
        return f"<Location: {self.name}>"
