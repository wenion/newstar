from h.models import CostItem

from h.i18n import TranslationString as _
from h.services.user_unique import DuplicateUserError


class CostItemService:
    """A service for manipulating organizations."""

    def __init__(self, session):
        """
        Create a new organizations service.

        :param session: the SQLAlchemy session object
        """
        self.session = session

    def get_by_id(self, id):
        """
        Get an organization by public id.

        :param pubid: The public id to search for
        :return: An organization model or None if no match is found
        """
        return self.session.query(CostItem).filter_by(id=id).one_or_none()

    def ensure_unique(self, number):
        errors = []

        if self.session.query(CostItem).filter_by(number=number).first():
            errors.append(
                _("user with number '{}' already exists".format(number))
            )

        if errors:
            raise DuplicateUserError(", ".join(errors))


def cost_item_factory(_context, request):
    return CostItemService(session=request.db)
