from sqlalchemy import func, cast, String

from h.models import RegistrationTermOption, RegistrationSourceOption, Registration


class RegistrationTermOptionService:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(RegistrationTermOption).filter_by(id=id).one_or_none()

    def get_all(self):
        return self.session.query(RegistrationTermOption).all()


class RegistrationSourceOptionService:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(RegistrationSourceOption).filter_by(id=id).one_or_none()

    def get_all(self):
        return self.session.query(RegistrationSourceOption).all()


class RegistrationService:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(Registration).filter_by(id=id).one_or_none()

    def get_list(self):
        combined_name_day = func.concat(
            Registration.last_name, ' ',
            Registration.first_name, ', ',
            Registration.email)
        return self.session.query(cast(func.min(Registration.id), String), combined_name_day) \
                .group_by(Registration.last_name, Registration.first_name, Registration.email).all()


def registration_term_option_factory(_context, request):
    return RegistrationTermOptionService(session=request.db)


def registration_source_option_factory(_context, request):
    return RegistrationSourceOptionService(session=request.db)


def registration_factory(_context, request):
    return RegistrationService(session=request.db)
