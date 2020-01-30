from functools import partial

from . import Base
from ..entities import Export
from ..paginated_results import PaginatedResults


class Exports(Base):
    EXPORTS_PATH = "/v1/data-exports"

    def fetch_all(self, limit: int = 5, **filters):
        args = {"limit": limit}

        if filters:
            for attribute, value in filters.items():
                args[attribute] = value

        response = self.request(self.EXPORTS_PATH).set_query_params(args).get()

        next_page = partial(self.fetch_all, limit=limit, **filters)
        return PaginatedResults(response.json, Export, next_page)

    def fetch(self, export_id: str = None, limit: int = 5, **filters):
        if export_id is None:
            return self.fetch_all(limit=limit, **filters)
        else:
            response = self.request(f"{self.EXPORTS_PATH}/{export_id}").get()
            return Export(response.json)
