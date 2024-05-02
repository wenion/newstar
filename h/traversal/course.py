from dataclasses import dataclass

from h.models import Course


@dataclass
class CourseContext:
    """Context for term-based views."""

    course: Course = None


class CourseRoot:
    """Root factory for routes which deal with terms."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        course = self.request.find_service(name="course").get_by_id(
            id
        )
        if course is None:
            raise KeyError()

        return CourseContext(course=course)
