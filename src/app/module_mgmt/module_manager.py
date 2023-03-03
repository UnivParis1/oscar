import os
from dataclasses import dataclass, field
from typing import Callable

import yaml
from yaml import SafeLoader

from app.module_mgmt.module import Module
from app.module_mgmt.module_factory import ModuleFactory


@dataclass
class ModuleManager:
    conf_dir: str
    modules: dict[str, Module] = field(default_factory=dict)
    files: [str] = field(default_factory=list)

    def __post_init__(self):
        self.files = os.listdir(self.conf_dir)

    @property
    def nb_modules(self):
        return len(self.files)

    class ModuleInitIterator:

        def __init__(self, manager, success_log_fn: Callable, error_log_fn: Callable):
            self.manager = manager
            self.success_log_fn = success_log_fn
            self.error_log_fn = error_log_fn
            self.counter = 0
            self.file_iterator = iter(self.manager.files)

        def __iter__(self):
            return self

        def __next__(self):
            filename = next(self.file_iterator)
            file = os.path.join(self.manager.conf_dir, filename)
            with open(file, encoding="utf-8") as yaml_file:
                self.success_log_fn(f"\u2192 Fichier d'initialisation découvert : {file}")
                data = yaml.load(yaml_file, Loader=SafeLoader)
                module = ModuleFactory.build(data['module'])
                self.manager.modules[module.identifier] = module
                self.success_log_fn(f"      \uFF0A Module : {module.identifier} initialisé avec succès")
                return module.identifier

    def init_iterator(self, success_log_fn: Callable, error_log_fn: Callable):
        """Discovers module configurations and instantiate modules

        """
        return ModuleManager.ModuleInitIterator(self, success_log_fn=success_log_fn, error_log_fn=error_log_fn)

    # yield counter
    def has_module(self, source: str) -> bool:
        pass
