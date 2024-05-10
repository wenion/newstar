"""Remove time column and add start time and end time columns"""

import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


revision = "bafd87159e12"
down_revision = "112ac1820527"

Session = orm.sessionmaker()

Course = sa.table(
    "course",
    sa.column("id", sa.Integer),
    sa.column("time", sa.UnicodeText),
    sa.column("start_time", sa.Time),
    sa.column("end_time", sa.Time),
)


def upgrade():
    op.add_column("course", sa.Column("start_time", sa.Time, nullable=True))
    op.add_column("course", sa.Column("end_time", sa.Time, nullable=True))

    bind = op.get_bind()
    session = Session(bind=bind)
    for item in session.query(Course).all():
        id = item[0]
        time = item[1]
        dt = datetime.datetime.strptime(time, '%H%M') 
        t = datetime.time(dt.hour, dt.minute, 0)
        op.execute(
            Course.update()
            .where(
                Course.c.id == id
            )
            .values(start_time = t)
        )

    op.drop_column("course", "time")


def downgrade():
    op.add_column("course", sa.Column("time", sa.UnicodeText, nullable=True))

    bind = op.get_bind()
    session = Session(bind=bind)
    for item in session.query(Course).all():
        id = item[0]
        start_time = item[2]
        time_str = start_time.strftime('%H%M')
        op.execute(
            Course.update()
            .where(
                Course.c.id == id
            )
            .values(time = time_str)
        )

    op.drop_column("course", "end_time")
    op.drop_column("course", "start_time")
