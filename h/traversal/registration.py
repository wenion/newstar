from dataclasses import dataclass

from h.models import RegistrationTermOption, RegistrationSourceOption, Registration


@dataclass
class RegistrationTermOptionContext:
    """Context for plan-based views."""

    opt: RegistrationTermOption = None


class RegistrationTermOptionRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        opt = self.request.find_service(name="registration_term_option").get_by_id(
            id
        )
        if opt is None:
            raise KeyError()

        return RegistrationTermOptionContext(opt=opt)


@dataclass
class RegistrationSourceOptionContext:
    """Context for plan-based views."""

    opt: RegistrationSourceOption = None


class RegistrationSourceOptionRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        opt = self.request.find_service(name="registration_source_option").get_by_id(
            id
        )
        if opt is None:
            raise KeyError()

        return RegistrationSourceOptionContext(opt=opt)


@dataclass
class RegistrationContext:
    """Context for plan-based views."""

    registration: Registration = None


class RegistrationRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        registration = self.request.find_service(name="registration").get_by_id(
            id
        )
        if registration is None:
            raise KeyError()

        return RegistrationContext(registration=registration)
