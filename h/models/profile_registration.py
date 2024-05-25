import sqlalchemy as sa

from h.db import Base, mixins


class ProfileRegistration(Base, mixins.Timestamps):
    __tablename__ = "profile_registration"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    profile_id = sa.Column(sa.Integer, sa.ForeignKey("profile.id", ondelete="CASCADE"), nullable=True)
    profile = sa.orm.relationship("Profile")

    registration_id = sa.Column(sa.Integer, sa.ForeignKey("registration.id", ondelete="CASCADE"), nullable=True)
    registration = sa.orm.relationship("Registration")

    def __repr__(self):
        return f"<ProfileRegistration: {str(self.id) + ' | profile: ' + str(self.profile_id) + ', registration: ' + str(self.registration_id)}>"
