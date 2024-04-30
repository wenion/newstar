import sqlalchemy as sa

from h.db import Base, mixins


class Term(Base, mixins.Timestamps):
    __tablename__ = "term"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), server_default="Term", nullable=False)

    number = sa.Column(sa.Integer, nullable=False)

    year = sa.Column(sa.Integer, nullable=False, index=True)

    start_date = sa.Column("start_date", sa.DateTime, nullable=True)
    end_date = sa.Column("end_date", sa.DateTime, nullable=True)

    number_of_weeks = sa.Column(sa.Integer, nullable=False)

    def __repr__(self):
        return f"<Term: {self.name + str(self.number) + '(' + str(self.year)+ ')'}>"
