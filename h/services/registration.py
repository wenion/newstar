from sqlalchemy import func, cast, String

from h.models import Course
from h.models import Level
from h.models import Profile
from h.models import ProfileRegistration
from h.models import RegistrationTermOption, RegistrationSourceOption, Registration


class RegistrationTermOptionService:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(RegistrationTermOption).filter_by(id=id).one_or_none()

    def get_list(self):
        return self.session.query(cast(func.min(RegistrationTermOption.id), String), RegistrationTermOption.name) \
            .group_by(RegistrationTermOption.id, RegistrationTermOption.name) \
            .order_by(RegistrationTermOption.id.asc()).all()


class RegistrationSourceOptionService:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(RegistrationSourceOption).filter_by(id=id).one_or_none()

    def get_list(self):
        return self.session.query(cast(func.min(RegistrationSourceOption.id), String), RegistrationSourceOption.name) \
            .group_by(RegistrationSourceOption.id, RegistrationSourceOption.name)\
            .order_by(RegistrationSourceOption.id.asc()).all()


class RegistrationService:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return (
            self.session.query(
                Registration.id.label('id'),
                Registration.created,
                Registration.updated,
                Registration.first_name,
                Registration.last_name,
                Registration.date_of_birth,
                Registration.gender,

                Registration.wechat,
                Registration.email,
                Registration.phone,
                Registration.first_emergency_contact,
                Registration.second_emergency_contact,
                Registration.emergency_contact,

                Level.id.label('level_id'),
                Level.abbreviation,

                # Location.id,
                # Location.abbreviation,

                Course.id.label('code_id'),
                Course.code,
                Course.day,
                # Course.start_time,

                RegistrationTermOption.id.label('term_id'),
                # RegistrationTermOption.name,

                RegistrationSourceOption.id.label('source_id'),
                # RegistrationSourceOption.name,

                ProfileRegistration.profile_id.label('profile_id'),
                Profile,
                ProfileRegistration.registration_id.label('registration_id'),

                Registration.referer,
                Registration.memeo,
                Registration.privacy_accepted,
                )
            .join(ProfileRegistration, Registration.id == ProfileRegistration.registration_id, isouter=True)
            .join(Profile, Profile.id == ProfileRegistration.profile_id, isouter=True)
            .join(Level, Level.id == Registration.level_id)
            .join(Course, Course.id == Registration.code_id)
            .join(RegistrationTermOption, RegistrationTermOption.id == Registration.term_id)
            .join(RegistrationSourceOption, RegistrationSourceOption.id == Registration.source_id)
            .filter(Registration.id==id)
            .one_or_none()
        )

    def get_list(self):
        combined_name = func.concat(
            Registration.id, ' - ',
            Registration.last_name, ' ',
            Registration.first_name, ', ',
            Registration.email)
        return self.session.query(cast(func.min(Registration.id), String), combined_name) \
                .group_by(Registration.id, Registration.last_name, Registration.first_name, Registration.email) \
                .order_by(Registration.id.asc()).all()

    # def get_unused_list(self):
    #     combined_name = func.concat(
    #         Registration.id, ' - ',
    #         Registration.last_name, ' ',
    #         Registration.first_name, ', ',
    #         Registration.email)
    #     return self.session.query(cast(func.min(Registration.id), String), combined_name) \
    #             .filter(Registration.profile == None) \
    #             .group_by(Registration.id, Registration.last_name, Registration.first_name, Registration.email) \
    #             .order_by(Registration.id.asc()).all()


def registration_term_option_factory(_context, request):
    return RegistrationTermOptionService(session=request.db)


def registration_source_option_factory(_context, request):
    return RegistrationSourceOptionService(session=request.db)


def registration_factory(_context, request):
    return RegistrationService(session=request.db)
