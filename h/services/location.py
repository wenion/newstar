import sqlalchemy as sa
from h.models import Location


class LocationService:
    """A service for manipulating organizations."""

    def __init__(self, session):
        """
        Create a new organizations service.

        :param session: the SQLAlchemy session object
        """
        self.session = session

    def create(self, name, abbreviation, address):
        """
        Create a new organization.

        An organization is a group of groups.

        :param name: the human-readable name of the organization
        :param authority: the authority to which the organization belongs
        :param logo: the logo of the organization in svg format

        :returns: the created organization
        """
        location = Location(name=name, abbreviation=abbreviation, address=address)
        self.session.add(location)
        return location

    def get_by_id(self, id):
        """
        Get an organization by public id.

        :param pubid: The public id to search for
        :return: An organization model or None if no match is found
        """
        return self.session.query(Location).filter_by(id=id).one_or_none()

    def get_by_name(self, name):
        return self.session.query(Location).filter(sa._or(Location.name==name, Location.abbreviation==name)).all()

    def get_all(self):
        return self.session.query(Location).all()


def location_factory(_context, request):
    """Return a OrganizationService instance for the request."""
    return LocationService(session=request.db)
