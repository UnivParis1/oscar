import pytest

import modules.dummy.module
from app.module_mgmt.module_manager import ModuleManager


class TestModuleManager:
    def test_init_dummy_module(self, capsys):
        module_manager = ModuleManager(conf_dir="tests_dummy_mod_conf")
        it = module_manager.init_iterator(error_log_fn=print, success_log_fn=print)
        for _ in it:
            pass
        assert module_manager.nb_modules == 1
        assert isinstance(module_manager.modules['dummy'], modules.dummy.module.Module)

    def test_init_dummy_module_output(self, capsys):
        module_manager = ModuleManager(conf_dir="tests_dummy_mod_conf")
        it = module_manager.init_iterator(error_log_fn=print, success_log_fn=print)
        for _ in it:
            pass
        out, err = capsys.readouterr()
        assert "Module : dummy initialisé avec succès" in out

    def test_init_missing_module(self):
        module_manager = ModuleManager(conf_dir="tests_missing_mod_conf")
        with pytest.raises(ModuleNotFoundError):
            it = module_manager.init_iterator(error_log_fn=print, success_log_fn=print)
            for _ in it:
                pass
