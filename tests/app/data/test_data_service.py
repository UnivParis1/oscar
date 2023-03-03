from app.data.data_service import DataService
from app.module_mgmt.module_manager import ModuleManager


class TestInputController:

    def test_data_service_return(self):
        module_manager = ModuleManager(conf_dir="tests_dummy_mod_conf")
        data_service = DataService(module_manager=module_manager)
        list(module_manager.init_iterator(error_log_fn=print, success_log_fn=print))
        entities = data_service.entities(entity_type="structure", field="acronym", value="LAMOP")
        entity = next(entities)
        assert type(entity).__name__ == "Structure", "Entity is a structure"
        assert entity.acronym == "LAMOP", "Entity acronym is 'LAMOP'"

    def test_data_service_not_found_behavior(self):
        module_manager = ModuleManager(conf_dir="tests_dummy_mod_conf")
        data_service = DataService(module_manager=module_manager)
        list(module_manager.init_iterator(error_log_fn=print, success_log_fn=print))
        entities = data_service.entities(entity_type="structure", field="acronym", value="MISSING")
        entity = next(entities)
        assert type(entity).__name__ == "Error", "Entity is a en error"
        assert entity.message == 'Entity with field value MISSING is never found by dummy module', "Entity has the right message"
