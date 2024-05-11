from sqlalchemy import func, cast, case, String

from h.models import Course

day_order = {
    '': Course.code,
    None: Course.code,
}

class CourseService:
    """A service for manipulating organizations."""

    def __init__(self, session, location_get_service, level_get_service):
        """
        Create a new organizations service.

        :param session: the SQLAlchemy session object
        """
        self.session = session
        self.location_get_service = location_get_service
        self.level_get_service = level_get_service

    def get_by_id(self, id):
        """
        Get an organization by public id.

        :param pubid: The public id to search for
        :return: An organization model or None if no match is found
        """
        return self.session.query(Course).filter_by(id=id).one_or_none()

    def get_by_code(self, code):
        return self.session.query(Course).filter_by(code=code).one_or_none()

    def get_list(self):
        combined_name = case(day_order, value=Course.memeo, else_= Course.code + ' (' + Course.memeo + ')')
        return self.session.query(cast(func.min(Course.id), String), combined_name) \
                .group_by(Course.code, Course.memeo) \
                .order_by(Course.code).all()


def course_factory(_context, request):
    """Return a OrganizationService instance for the request."""
    return CourseService(
        session=request.db,
        location_get_service=request.find_service(name="location"),
        level_get_service=request.find_service(name="level"),
    )
