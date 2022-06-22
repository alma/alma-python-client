from collections.abc import Iterable
from typing import Callable, Type

from alma_client.entities import Base as BaseEntity


class PaginatedResults(Iterable):
    def __init__(self, data: dict, entity: Type[BaseEntity], next_page: Callable):
        self._data = data
        self._entities = [entity(d) for d in data.get("data", [])]
        self._next_page = next_page

    def __getitem__(self, i: int) -> BaseEntity:
        return self._entities[i]

    def __iter__(self):
        return iter(self._entities)

    def __len__(self):
        return len(self._entities)

    def next_page(self):
        if not self._data.get("has_more"):
            return PaginatedResults({}, BaseEntity, None)

        return self._next_page(starting_after=self._entities[-1].id)
