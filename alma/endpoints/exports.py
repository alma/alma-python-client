from functools import partial
from datetime import datetime
from io import BytesIO

from . import Base
from ..entities import Export
from ..paginated_results import PaginatedResults


EXPORT_TYPES = ['payments', 'accounting', 'accounting_for_payout']


class ExportsException(Exception):
    pass


class Exports(Base):
    EXPORTS_PATH = "/v1/data-exports"

    def create(self, export_type: str = None, payout_id: str = None,
               start: datetime = None, end: datetime = None):
        """ Create a new export"""
        if export_type not in EXPORT_TYPES:
            raise ExportsException("%s is not an availale type" % export_type)

        data = {"type": export_type}
        if payout_id:
            data['payout'] = payout_id

        if start:
            data['start'] = int(start.timestamp())

        if end:
            data['end'] = int(end.timestamp())

        response = self.request(self.EXPORTS_PATH).set_body(data).post()
        return Export(response.json)

    def get_file(self, export_id: str = None, export_format: str = 'csv'):
        if export_id is None:
            raise ExportsException('export_id is required')

        request = self.request(f"{self.EXPORTS_PATH}/{export_id}")
        request.set_query_params(dict(format=export_format))
        response = request.get()
        return BytesIO(response.resp.text.encode())

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
