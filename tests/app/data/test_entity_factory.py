import pytest

from app.data.data_service import DataService
from app.data.entity_factory import EntityFactory
from app.module_mgmt.module_manager import ModuleManager


class TestEntityFactory:

    def test_entity_factory_creates_structure(self):
        entity_class = EntityFactory.entity_class("structure")
        assert entity_class.__name__ == "Structure"
    def test_entity_factory_creates_structure_with_default_field(self):
        entity_class = EntityFactory.entity_class("structure", "code", "1234")
        entity = entity_class()
        assert entity_class.rnsr_id == "1234"

    def test_entity_factory_exception(self):
        with pytest.raises(ValueError):
            EntityFactory.entity_class("foobar")
