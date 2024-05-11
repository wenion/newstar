import sqlalchemy as sa

from h.db import Base, mixins


class CostItem(Base, mixins.Timestamps):
    __tablename__ = "cost_item"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    number = sa.Column(sa.UnicodeText(), nullable=True, unique=True)
    name = sa.Column("name", sa.UnicodeText(), nullable=True)
    price = sa.Column("price", sa.Float(), nullable=True)
    gst_included = sa.Column("gst_included", sa.Float(), nullable=True)
    comments = sa.Column("comments", sa.UnicodeText(), nullable=True)

    level_id = sa.Column(sa.Integer, sa.ForeignKey("level.id"), nullable=True)
    level = sa.orm.relationship("Level", backref="cost_item")

    term_id = sa.Column(sa.Integer, sa.ForeignKey("term.id"), nullable=True)
    term = sa.orm.relationship("Term", backref="cost_item")

    def __repr__(self):
        return f"<Cost Item: {self.number + self.name}>"
