from dataclasses import dataclass

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
        return (modules[module].entity(entity_type=entity_type, field=field, value=value)
                for module in iter(modules))
