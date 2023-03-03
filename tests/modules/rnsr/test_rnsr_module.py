from pathlib import Path
from unittest.mock import patch

from app.module_mgmt.module_manager import ModuleManager
from modules.rnsr.rnsr_module import RnsrModule


class TestRnsrModule:

    def test_lamop_title(self):
        rnsr_module = self._init_rnsr_module()
        with patch.object(RnsrModule, '_get_entity_result_page',
                          return_value=self._read_result_page(rnsr_module, page="lamop.html")):
            entity = rnsr_module.entity("structure", "acronym", "LAMOP")
            assert entity.title == 'Laboratoire de Médiévistique Occidentale de Paris ', "Entity title is 'Laboratoire de Médiévistique Occidentale de Paris '"

    def test_lamop_rnsr_id(self):
        rnsr_module = self._init_rnsr_module()
        with patch.object(RnsrModule, '_get_entity_result_page',
                          return_value=self._read_result_page(rnsr_module, page="lamop.html")):
            entity = rnsr_module.entity("structure", "acronym", "LAMOP")
            assert entity.rnsr_id == '199812917D', "Entity RNSR id is '199812917D'"

    def test_lamop_address(self):
        rnsr_module = self._init_rnsr_module()
        with patch.object(RnsrModule, '_get_entity_result_page',
                          return_value=self._read_result_page(rnsr_module, page="lamop.html")):
            entity = rnsr_module.entity("structure", "acronym", "LAMOP")
            assert entity.address == 'Centre Sorbonne, 17 rue de la Sorbonne 75005 PARIS ', "Entity address is 'Centre Sorbonne, 17 rue de la Sorbonne 75005 PARIS '"

    def _read_result_page(self, rnsr_module, page):
        driver = rnsr_module._get_web_driver()
        driver.get(f"file://{Path('fixtures/rnsr/' + page).resolve()}")
        return driver

    def _init_rnsr_module(self):
        module_manager = ModuleManager(conf_dir="conf/test_rnsr_module_conf")
        init_iterator = module_manager.init_iterator(error_log_fn=print, success_log_fn=print)
        for _ in init_iterator:
            pass
        assert module_manager.nb_modules == 1
        rnsr_module: RnsrModule = module_manager.modules['rnsr']
        return rnsr_module
