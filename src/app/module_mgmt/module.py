import abc
from dataclasses import dataclass
from typing import Iterator

from app.data.entity_factory import EntityFactory


@dataclass
class Module(abc.ABC):
    identifier: str
    name: str

    @abc.abstractmethod
    def entity(self, entity_type: str, field: str, value: str) -> dict:
        return EntityFactory.entity_class(entity_type, field, value, self.identifier)()

    @abc.abstractmethod
    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass
