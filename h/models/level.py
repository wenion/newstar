import sqlalchemy as sa

from h.db import Base, mixins


class Level(Base, mixins.Timestamps):
    __tablename__ = "level"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), nullable=False)

    abbreviation = sa.Column("abbreviation", sa.UnicodeText(), nullable=False)

    start_age = sa.Column("start_age", sa.UnicodeText(), nullable=True)
    end_age = sa.Column("end_age", sa.UnicodeText(), nullable=True)

    def __repr__(self):
        return f"<Level: {self.name}>"
