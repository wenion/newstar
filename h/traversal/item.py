from dataclasses import dataclass

from h.models import CostItem


@dataclass
class CostItemContext:
    """Context for plan-based views."""

    cost_item: CostItem = None


class CostItemRoot:
    """Root factory for routes which deal with plans."""

    def __init__(self, request):
        self.request = request

    def __getitem__(self, id):
        cost_item = self.request.find_service(name="cost_item").get_by_id(
            id
        )
        if cost_item is None:
            raise KeyError()

        return CostItemContext(cost_item=cost_item)
