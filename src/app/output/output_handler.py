import abc
from typing import Generator

from app.data.entity_factory import EntityFactory


class OutputHandler(abc.ABC):

    def __init__(self):
        self.base_class = None
        self.entity_type = None
        self.search_field = None
        self.requested_value = None
        self.expected_modules_count = None

    @staticmethod
    def _error_entity(entity):
        return type(entity).__name__ == 'Error'

    def set_mode(self, entity_type: str, search_field: str, requested_value: str, expected_modules_count: int):
        self.entity_type = entity_type
        self.search_field = search_field
        self.requested_value = requested_value
        self.expected_modules_count = expected_modules_count
        self.base_class = EntityFactory.entity_class(entity_type)
        return self

    @abc.abstractmethod
    def output(self, entities_gen: Generator[object, None, None]):
        pass
