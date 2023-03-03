from unittest.mock import patch, MagicMock

import pytest

from app.data.data_service import DataService
from app.module_mgmt.module_manager import ModuleManager
from app.output.prompt_output_handler import PromptOutputHandler
from app.input_controller import InputController


class TestInputController:

    @patch.object(PromptOutputHandler, 'output')
    def test_input_controller_return(self, mock: MagicMock):
        controller = self.build_controller()
        controller.handle("A=LAMOP", entity_type="structure")
        assert 'entities_gen' in mock.call_args.kwargs, "Ouput method called with entities_gen argument"
        result_generator = mock.call_args.kwargs['entities_gen']
        first_result = next(result_generator)
        assert first_result.acronym == 'LAMOP', "Acronym of first result is 'LAMOP'"

    def test_input_controller_raises_value_error(self):
        controller = self.build_controller()
        with pytest.raises(ValueError):
            controller.handle("foobar", entity_type="structure")

    def test_input_controller_raises_keyboard_interrupt(self):
        controller = self.build_controller()
        with pytest.raises(KeyboardInterrupt):
            controller.handle("Q", entity_type="structure")

    def test_input_controller_iterative_initialisation(self):
        module_manager = ModuleManager(conf_dir="conf/tests_dummy_mod_conf")
        data_service = DataService(module_manager=module_manager)
        controller = InputController(data_service=data_service, output_handler=PromptOutputHandler(),
                                     error_logger=print, info_logger=print, success_logger=print)
        gen = controller.iterative_initializer()
        assert next(gen) == "dummy"

    def build_controller(self):
        module_manager = ModuleManager(conf_dir="conf/tests_dummy_mod_conf")
        data_service = DataService(module_manager=module_manager)
        controller = InputController(data_service=data_service, output_handler=PromptOutputHandler(),
                                     error_logger=print, info_logger=print, success_logger=print)
        list(controller.iterative_initializer())
        return controller
