from dataclasses import dataclass

from app.data.entity_factory import EntityFactory
from app.module_mgmt.exceptions import EntityNotFoundError, DuplicateEntitiesError, ConnectionFailureError
from app.module_mgmt.module_manager import ModuleManager


@dataclass
class DataService:
    module_manager: ModuleManager

    def values_for(self, entity_type, field, source):
        if not self.module_manager.has_module(source):
            raise ValueError(f"No source module for key {source}")
        return self.module_manager.modules[source].values_for(entity_type, field)

    def entities(self, entity_type, field, value):
        modules = self.module_manager.modules
        for module in iter(modules):
            try:
                yield modules[module].entity(entity_type=entity_type, field=field, value=value)
            except (EntityNotFoundError, DuplicateEntitiesError, ConnectionFailureError) as error:
                yield EntityFactory.entity_class("error", "message", str(error), module)()
