import importlib

from app.module_mgmt.module import Module


class ModuleFactory:

    @staticmethod
    def camel_case(string):
        return ''.join(map(lambda word: word.capitalize(), string.split("_")))

    @classmethod
    def build(cls, config: dict) -> Module:
        module_class = getattr(importlib.import_module(f"modules.{config['id']}.{config['id']}_module"),
                               cls.camel_case(f"{config['id']}_module"))
        module = module_class(identifier=config["id"], name=config["name"], config=config["config"])
        return module
