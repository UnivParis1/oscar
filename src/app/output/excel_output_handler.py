from typing import Generator

from app.output.output_handler import OutputHandler


class ExcelOutputHandler(OutputHandler):
    def output(self, entities_gen: Generator[object, None, None]):
        entities = list(entities_gen)
        entities
