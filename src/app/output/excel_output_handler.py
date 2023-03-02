from typing import Generator

from app.output.output_handler import OutputHandler


class ExcelOutputHandler(OutputHandler):
    def format(self, entity_type: str, field: str, value: str, entities_gen: Generator[object, None, None], nb_modules: int):
        pass
