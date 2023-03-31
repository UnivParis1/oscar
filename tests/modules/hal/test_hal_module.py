from pathlib import Path
from unittest.mock import patch

import pandas as pd

from app.module_mgmt.module_manager import ModuleManager
from modules.hal.hal_module import HalModule


class TestHalModule:

    def test_cri_title(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "acronym", "CRI")
            assert entity.title == 'Centre de Recherche en Informatique de Paris 1', "Entity title should be 'Centre de Recherche en Informatique de Paris 1'"

    def test_cri_rnsr_id(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "acronym", "CRI")
            assert entity.rnsr_id == '199213454N', "Entity RNSR id should be '199213454N'"

    def test_cri_number(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "acronym", "CRI")
            assert entity.number == 'EA1445', "Entity number should be 'EA1445'"

    def test_cri_address(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "acronym", "CRI")
            assert entity.address == 'Université Paris 1 Panthéon-Sorbonne 90 rue de Tolbiac 75013 Paris Pays FR', "Entity address should be 'Université Paris 1 Panthéon-Sorbonne 90 rue de Tolbiac 75013 Paris Pays FR'"

    def test_cri_url(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "acronym", "CRI")
            assert entity.url == 'https://cri.pantheonsorbonne.fr/', "Entity website URL should be 'https://cri.pantheonsorbonne.fr/'"

    def test_title_by_code(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "number", "UR4100")
            assert entity.title == "Histoire culturelle et sociale de l'art", "Entity title should be 'Histoire culturelle et sociale de l\'art'"

    def test_acronym_by_title(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "title", "Laboratoire de Médiévistique Occidentale de Paris")
            assert entity.acronym == "LAMOP", "Entity acronym should be 'LAMOP'"

    def test_acronym_by_title_pattern(self):
        hal_module = self._init_hal_module()
        with patch.object(HalModule, '_get_hal_research_structures',
                          return_value=self._hal_data_file("default.json")):
            entity = hal_module.entity("structure", "title", "*médiévistique*")
            assert entity.acronym == "LAMOP", "Entity acronym should be 'LAMOP'"

    def _hal_data_file(self, name):
        file_location = f"file://{Path('fixtures/hal/' + name).resolve()}"
        file_path = Path(file_location)
        return pd.read_json(file_path)

    def _init_hal_module(self) -> HalModule:
        module_manager = ModuleManager(conf_dir="conf/test_hal_module_conf")
        for _ in module_manager.init_iterator(error_log_fn=print, success_log_fn=print):
            pass
        return module_manager.modules['hal']
