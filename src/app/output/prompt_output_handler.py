import dataclasses
from typing import Generator

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import ProgressBar

from app.output.label_table import LabelTable
from app.output.output_handler import OutputHandler


class PromptOutputHandler(OutputHandler):
    def output(self, entities_gen: Generator[object, None, None]):
        assert self.base_class is not None, "Configure output with 'set_mode' before sending entities"
        entities = {}
        with ProgressBar(title="Interrogation des sources") as pb:
            for _ in pb(range(self.expected_modules_count), label="Interrogation des sources"):
                source = next(entities_gen)
                pb.title = f"Interrogation en cours {source.source}"
                entities[source.source] = source
                if self._error_entity(source):
                    print_formatted_text(HTML(f"<b><red>Source : {source.source} Erreur : {source.message}</red></b>"))
            pb.title = "Interrogation des sources terminée"
        for search_field in dataclasses.fields(self.base_class):
            if search_field.name in ['source']:
                continue
            print_formatted_text(HTML(f"<b><green>Champ : {LabelTable.FIELDS[search_field.name]}</green></b><br/>"))
            for source in entities:
                entity = entities[source]
                if self._error_entity(entity):
                    print_formatted_text(HTML(f"<b><red>Source : {source} Erreur : {entity.message}</red></b>"))
                else:
                    print_formatted_text(
                        HTML(f"<green>{source} : {getattr(entity, search_field.name)}</green>"))
