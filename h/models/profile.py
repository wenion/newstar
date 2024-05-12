import sqlalchemy as sa

from h.db import Base, mixins


class Profile(Base, mixins.Timestamps):
    __tablename__ = "profile"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    number = sa.Column(sa.UnicodeText(), nullable=True, unique=True)
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

    memeo = sa.Column("memeo", sa.UnicodeText(), nullable=True)

    registration_id = sa.Column(sa.Integer, sa.ForeignKey("registration.id"), nullable=True)
    registration = sa.orm.relationship("Registration", backref="profile")

    referer_id = sa.Column(sa.Integer, sa.ForeignKey("profile.id"), nullable=True)
    referer = sa.orm.relationship("Profile", backref="referrals", remote_side="Profile.id")

    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=True)
    user = sa.orm.relationship("User", backref="profile", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Profile: {str(self.id) + ' ' + self.number + ' ' + self.first_name}>"
