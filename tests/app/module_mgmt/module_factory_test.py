import modules.dummy.module
from app.module_mgmt.module_factory import ModuleFactory


class TestModuleFactory:
    def test_init_dummy_module(self, capsys):
        module = ModuleFactory.build({'id': 'dummy', 'name': 'Dummy module',
                                      'config': None})
        assert isinstance(module, modules.dummy.module.Module)

    def test_init_hal_module(self, capsys):
        module = ModuleFactory.build({'id': 'hal', 'name': 'Hal module',
                                      'config': None})
        assert isinstance(module, modules.hal.module.Module)
