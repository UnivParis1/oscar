from typing import Iterator

from app.module_mgmt.module import Module


class Module(Module):
    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass

    def entity(self, entity_type: str, field: str, value: str) -> object:
        entity = super().entity(entity_type=entity_type, field=field, value=value)
        return entity

