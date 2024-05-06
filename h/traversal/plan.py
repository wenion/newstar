from dataclasses import dataclass

from h.models import Plan


@dataclass
class PlanContext:
    """Context for plan-based views."""

    plan: Plan = None


class PlanRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        plan = self.request.find_service(name="plan").get_by_id(
            id
        )
        if plan is None:
            raise KeyError()

        return PlanContext(plan=plan)
