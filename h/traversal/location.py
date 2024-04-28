from dataclasses import dataclass

from h.models import Location


@dataclass
class LocationContext:
    """Context for organization-based views."""

    location: Location = None


class LocationRoot:
    """Root factory for routes which deal with organizations."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        location = self.request.find_service(name="location").get_by_id(
            id
        )
        if location is None:
            raise KeyError()

        return LocationContext(location=location)
