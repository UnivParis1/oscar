import pytest

import modules.dummy.dummy_module
from app.module_mgmt.module_manager import ModuleManager


class TestModuleManager:
    def test_init_dummy_module(self):
        module_manager = ModuleManager(conf_dir="conf/tests_dummy_mod_conf")
        for _ in module_manager.init_iterator(error_log_fn=print, success_log_fn=print):
            pass
        assert module_manager.nb_modules == 1
        assert isinstance(module_manager.modules['dummy'], modules.dummy.dummy_module.DummyModule)

    def test_init_dummy_module_output(self, capsys):
        module_manager = ModuleManager(conf_dir="conf/tests_dummy_mod_conf")
        for _ in module_manager.init_iterator(error_log_fn=print, success_log_fn=print):
            pass
        out, _ = capsys.readouterr()
        assert "Module : dummy initialisé avec succès" in out

    def test_init_missing_module(self):
        module_manager = ModuleManager(conf_dir="conf/tests_missing_mod_conf")
        with pytest.raises(ModuleNotFoundError):
            it = module_manager.init_iterator(error_log_fn=print, success_log_fn=print)
            for _ in it:
                pass
