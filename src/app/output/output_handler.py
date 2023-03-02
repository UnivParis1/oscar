import abc
from typing import Generator


class OutputHandler(abc.ABC):

    @abc.abstractmethod
    def format(self, entity_type: str, field: str, value: str, entities_gen: Generator[object, None, None],
               nb_modules: int):
        pass
