import dataclasses
from typing import Generator

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import ProgressBar

from app.output.label_table import LabelTable
from app.output.output_handler import OutputHandler


class PromptOutputHandler(OutputHandler):
    def format(self, entity_type: str, field: str, value: str, entities_gen: Generator[object, None, None], nb_modules: int):
        entities = {}
        with ProgressBar(title="Interrogation des sources") as pb:
            for _ in pb(range(nb_modules), label="Initialisation"):
                entity = next(entities_gen)
                pb.title = entity.source
                entities[entity.source] = entity
        object_class = type(list(entities.values())[0])
        for field in dataclasses.fields(object_class):
            if field.name in ['source']:
                continue
            print_formatted_text(HTML(f"<b><green>Champ : {LabelTable.FIELDS[field.name]}</green></b><br/>"))
            for entity in entities:
                print_formatted_text(
                    HTML(f"<li><green>{entity} : {getattr(entities[entity], field.name)}</green></li>"))
