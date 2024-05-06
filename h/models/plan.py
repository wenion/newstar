import sqlalchemy as sa

from h.db import Base, mixins


class Plan(Base, mixins.Timestamps):
    __tablename__ = "plan"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name = sa.Column("name", sa.UnicodeText(), nullable=False)

    code_id = sa.Column(sa.Integer, sa.ForeignKey("course.id"), nullable=False)
    code = sa.orm.relationship("Course", backref="plan")

    location_id = sa.Column(sa.Integer, sa.ForeignKey("location.id"), nullable=False)
    location = sa.orm.relationship("Location", backref="plan")

    level_id = sa.Column(sa.Integer, sa.ForeignKey("level.id"), nullable=False)
    level = sa.orm.relationship("Level", backref="plan")

    term_id = sa.Column(sa.Integer, sa.ForeignKey("term.id"), nullable=False)
    term = sa.orm.relationship("Term", backref="plan")

    start_time = sa.Column(sa.DateTime, nullable=False)
    end_time = sa.Column(sa.DateTime, nullable=False)
    memeo = sa.Column("memeo", sa.UnicodeText(), nullable=True)

    def __repr__(self):
        return f"<Plan: {self.name}>"
