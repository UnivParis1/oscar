import re
from dataclasses import dataclass
from typing import Callable

from app.data_service import DataService
from app.output.output_handler import OutputHandler


@dataclass
class InputController:
    data_service: DataService
    output_handler: OutputHandler
    error_logger: Callable
    info_logger: Callable
    success_logger: Callable

    PROMPT_REGEX = re.compile('([ACNTacnt])(=|:)(.+)$')
    FIELDS_INDEX = {
        'a': 'acronym',
        'c': 'code',
        'n': 'number',
        't': 'title',
    }

    def handle(self, user_input, entity_type):
        if user_input == 'Q':
            raise KeyboardInterrupt
        code, operator, user_value = self.parse_user_input(user_input)
        field_name = self.FIELDS_INDEX[code.lower()]
        if operator == ":":
            values = self.data_service.values_for(entity_type=entity_type, field=field_name, source=user_value)
            for value in values:
                entities_gen = self.data_service.entities(entity_type=entity_type, field=field_name, value=value)
                self.output_handler.format(entity_type=entity_type, field=field_name, value=value,
                                           entities_gen=entities_gen,
                                           nb_modules=self.data_service.module_manager.nb_modules)
        elif operator == "=":
            self.info_logger(f"\u2699 Contrôle d'alignement d'entité : critère [{field_name}]=[{user_value}]")
            entities_gen = self.data_service.entities(entity_type=entity_type, field=field_name, value=user_value)
            self.output_handler.format(entity_type=entity_type, field=field_name, value=user_value,
                                       entities_gen=entities_gen,
                                       nb_modules=self.data_service.module_manager.nb_modules)

    def parse_user_input(self, user_input):
        matching = self.PROMPT_REGEX.match(user_input)
        if matching is None:
            raise ValueError
        code = matching.group(1)
        operator = matching.group(2)
        value = matching.group(3)
        return code, operator, value

    def iterative_initializer(self):
        yield from self.data_service.module_manager.init_iterator(success_log_fn=self.success_logger,
                                                                  error_log_fn=self.error_logger)
