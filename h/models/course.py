import sqlalchemy as sa

from h.db import Base, mixins


class Course(Base, mixins.Timestamps):
    __tablename__ = "course"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    year = sa.Column(sa.Integer, nullable=False)

    location_id = sa.Column(sa.Integer, sa.ForeignKey("location.id"), nullable=True)
    location = sa.orm.relationship("Location", backref="course")

    day = sa.Column(sa.UnicodeText(), nullable=True)

    start_time = sa.Column(sa.Time, nullable=True)
    end_time = sa.Column(sa.Time, nullable=True)

    level_id = sa.Column(sa.Integer, sa.ForeignKey("level.id"), nullable=True)
    level = sa.orm.relationship("Level", backref="course")

    code = sa.Column("code", sa.UnicodeText(), nullable=False)
    memeo = sa.Column("memeo", sa.UnicodeText(), nullable=True)

    def __repr__(self):
        return f"<Course: {self.code}>"
