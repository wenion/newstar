from dataclasses import dataclass

from h.models import Level


@dataclass
class LevelContext:
    """Context for organization-based views."""

    level: Level = None


class LevelRoot:
    """Root factory for routes which deal with organizations."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        level = self.request.find_service(name="level").get_by_id(
            id
        )
        if level is None:
            raise KeyError()

        return LevelContext(level=level)
