from dataclasses import dataclass

from h.models import Profile


@dataclass
class ProfileContext:
    """Context for plan-based views."""

    profile: Profile = None


class ProfileRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        profile = self.request.find_service(name="profile").get_by_id(
            id
        )
        if profile is None:
            raise KeyError()

        return ProfileContext(profile=profile)
