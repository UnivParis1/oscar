from unittest.mock import patch, MagicMock

from app.data_service import DataService
from app.module_mgmt.module_manager import ModuleManager
from app.output.prompt_output_handler import PromptOutputHandler
from app.input_controller import InputController


class TestInputController:

    @patch.object(PromptOutputHandler, 'format')
    def test_input_controller_return(self, mock: MagicMock):
        module_manager = ModuleManager(conf_dir="tests_dummy_mod_conf")
        data_service = DataService(module_manager=module_manager)
        controller = InputController(data_service=data_service, output_handler=PromptOutputHandler(),
                                     error_logger=print, info_logger=print, success_logger=print)
        list(module_manager.init_iterator(error_log_fn=print, success_log_fn=print))
        controller.handle("A=LAMOP", entity_type="structure")
        result_generator = mock.call_args.kwargs['entities_gen']
        first_result = next(result_generator)
        assert first_result.acronym == 'LAMOP'
