from dataclasses import dataclass

from h.models import Term


@dataclass
class TermContext:
    """Context for term-based views."""

    term: Term = None


class TermRoot:
    """Root factory for routes which deal with terms."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        term = self.request.find_service(name="term").get_by_id(
            id
        )
        if term is None:
            raise KeyError()

        return TermContext(term=term)
