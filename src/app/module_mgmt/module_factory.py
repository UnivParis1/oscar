import importlib

from app.module_mgmt.module import Module


class ModuleFactory:
    @classmethod
    def build(cls, config: dict) -> Module:
        module_class = getattr(importlib.import_module(f"modules.{config['id']}.module"), "Module")
        module = module_class(id=config["id"], name=config["name"])
        return module
