from sqlalchemy import func, cast, String

from h.models import Profile
from h.i18n import TranslationString as _
from h.services.user_unique import DuplicateUserError


class ProfileService:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id):
        return self.session.query(Profile).filter_by(id=id).one_or_none()
    
    def get_account_by_id(self, id):
        return self.session.query(Profile).filter_by(user_id=id).one_or_none()

    def get_list(self, self_id = None):
        filter_terms = []
        if self_id:
            filter_terms.append(Profile.code_id == int(self_id))

        combined_name_day = func.concat(
            Profile.last_name, ' ',
            Profile.first_name, ', ',
            Profile.email)
        return self.session.query(cast(func.min(Profile.id), String), combined_name_day) \
                .filter_by(*filter_terms) \
                .group_by(Profile.last_name, Profile.first_name, Profile.email).all()

    def ensure_unique(self, number):
        errors = []

        if self.session.query(Profile).filter_by(number=number).first():
            errors.append(
                _("user with number '{}' already exists".format(number))
            )

        if errors:
            raise DuplicateUserError(", ".join(errors))


def profile_factory(_context, request):
    return ProfileService(session=request.db)
