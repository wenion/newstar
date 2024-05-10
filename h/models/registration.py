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


class Registration(Base, mixins.Timestamps):
    __tablename__ = "registration"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    first_name = sa.Column("first_name", sa.UnicodeText(), nullable=True)
    last_name = sa.Column("last_name", sa.UnicodeText(), nullable=True)
    date_of_birth = sa.Column(sa.DateTime, nullable=True)
    gender = sa.Column(sa.UnicodeText(), nullable=True)

    wechat = sa.Column(sa.UnicodeText())
    email = sa.Column(sa.UnicodeText())
    phone = sa.Column(sa.UnicodeText())
    first_emergency_contact = sa.Column(sa.UnicodeText())
    second_emergency_contact = sa.Column(sa.UnicodeText())
    emergency_contact = sa.Column(sa.UnicodeText())

    level_id = sa.Column(sa.Integer, sa.ForeignKey("level.id"), nullable=True)
    level = sa.orm.relationship("Level", backref="registration")

    location_id = sa.Column(sa.Integer, sa.ForeignKey("location.id"), nullable=True)
    location = sa.orm.relationship("Location", backref="registration")

    code_id = sa.Column(sa.Integer, sa.ForeignKey("course.id"), nullable=True)
    code = sa.orm.relationship("Course", backref="registration")

    term_id = sa.Column(sa.Integer, sa.ForeignKey("registration_term_option.id"), nullable=True)
    term = sa.orm.relationship("RegistrationTermOption", backref="registration")

    source_id = sa.Column(sa.Integer, sa.ForeignKey("registration_source_option.id"), nullable=True)
    source = sa.orm.relationship("RegistrationSourceOption", backref="registration")

    referer = sa.Column(sa.UnicodeText())
    memeo = sa.Column(sa.UnicodeText())
    privacy_accepted = sa.Column(sa.DateTime, nullable=True)

    def __repr__(self):
        return f"<Registration: {self.first_name + self.last_name}>"
