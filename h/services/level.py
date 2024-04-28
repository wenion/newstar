import sqlalchemy as sa
from h.models import Level


class LevelService:
    """A service for manipulating organizations."""

    def __init__(self, session):
        """
        Create a new organizations service.

        :param session: the SQLAlchemy session object
        """
        self.session = session

    def create(self, name, abbreviation, start_age, end_age):
        """
        Create a new organization.

        An organization is a group of groups.

        :param name: the human-readable name of the organization
        :param authority: the authority to which the organization belongs
        :param logo: the logo of the organization in svg format

        :returns: the created organization
        """
        level = Level(name=name, abbreviation=abbreviation, start_age=start_age, end_age=end_age)
        self.session.add(level)
        return level

    def get_by_id(self, id):
        """
        Get an organization by public id.

        :param pubid: The public id to search for
        :return: An organization model or None if no match is found
        """
        return self.session.query(Level).filter_by(id=id).one_or_none()

    def get_by_name(self, name):
        return self.session.query(Level).filter(sa._or(Level.name==name, Level.abbreviation==name)).all()


def level_factory(_context, request):
    """Return a OrganizationService instance for the request."""
    return LevelService(session=request.db)
