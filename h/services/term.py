from sqlalchemy import func, cast, String

from h.models import Term


class TermService:
    """A service for manipulating organizations."""

    def __init__(self, session):
        """
        Create a new organizations service.

        :param session: the SQLAlchemy session object
        """
        self.session = session

    def create(self, name, number, year, start_date, end_date, number_of_weeks):
        """
        Create a new organization.

        An organization is a group of groups.

        :param name: the human-readable name of the organization
        :param authority: the authority to which the organization belongs
        :param logo: the logo of the organization in svg format

        :returns: the created organization
        """
        term = Term(name=name, number=number, year=year, start_date=start_date, end_date=end_date, number_of_weeks=number_of_weeks)
        self.session.add(term)
        return term

    def get_by_id(self, id):
        """
        Get an organization by public id.

        :param pubid: The public id to search for
        :return: An organization model or None if no match is found
        """
        return self.session.query(Term).filter_by(id=id).one_or_none()

    def get_by_year(self, year):
        return self.session.query(Term).filter_by(year=year).all()

    def get_all(self):
        return self.session.query(Term).order_by(Term.year.asc(), Term.number.asc()).all()

    def get_list(self):
        combined_name = func.concat(Term.name, Term.number, ' (', Term.year, ')')
        return self.session.query(cast(func.min(Term.id), String), combined_name) \
                .group_by(Term.name, Term.number, Term.year).all()


def term_factory(_context, request):
    """Return a OrganizationService instance for the request."""
    return TermService(session=request.db)
