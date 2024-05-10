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


def registration_term_option_factory(_context, request):
    return RegistrationTermOptionService(session=request.db)


def registration_source_option_factory(_context, request):
    return RegistrationSourceOptionService(session=request.db)


def registration_factory(_context, request):
    return RegistrationService(session=request.db)
