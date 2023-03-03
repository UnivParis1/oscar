from app.module_mgmt.module_factory import ModuleFactory
from modules.dummy.dummy_module import DummyModule
from modules.hal.hal_module import HalModule


class TestModuleFactory:
    def test_init_dummy_module(self):
        module = ModuleFactory.build({'id': 'dummy', 'name': 'Dummy module',
                                      'config': None})
        assert isinstance(module, DummyModule)

    def test_init_hal_module(self):
        module = ModuleFactory.build({'id': 'hal', 'name': 'Hal module',
                                      'config': None})
        assert isinstance(module, HalModule)
