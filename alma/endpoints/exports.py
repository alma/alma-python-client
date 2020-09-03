from datetime import datetime
from functools import partial
from io import BytesIO

from ..entities import Export, ExportFormat, ExportType
from . import Base


class Exports(Base):
    EXPORTS_PATH = "/v1/data-exports"

    def create(
        self,
        export_type: ExportType,
        payout_id: str = None,
        start: datetime = None,
        end: datetime = None,
    ):
        """ Create a new export"""
        data = {"type": export_type.value}
        if payout_id:
            data["payout"] = payout_id

        if start:
            data["start"] = int(start.timestamp())

        if end:
            data["end"] = int(end.timestamp())

        return self.request(self.EXPORTS_PATH).set_body(data).post().expectJson(Export)

    def get_file(self, export_id: str, export_format: ExportFormat = None):
        request = self.request(f"{self.EXPORTS_PATH}/{export_id}")
        if export_format:
            request.set_query_params({"format": export_format.value})

        return request.get().expect(lambda response: BytesIO(response.resp.content))

    def fetch_all(self, limit: int = 5, **filters):
        args = {"limit": limit, **filters}
        next_page = partial(self.fetch_all, limit=limit, **filters)
        return (
            self.request(self.EXPORTS_PATH)
            .set_query_params(args)
            .get()
            .expectPaginatedList(Export, next_page)
        )

    def fetch(self, export_id: str = None, limit: int = 5, **filters):
        if export_id is None:
            return self.fetch_all(limit=limit, **filters)
        else:
            return self.request(f"{self.EXPORTS_PATH}/{export_id}").get().expectJson(Export)
