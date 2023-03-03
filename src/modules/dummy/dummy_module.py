from typing import Iterator

from app.module_mgmt.exceptions import EntityNotFoundError, DuplicateEntitiesError
from app.module_mgmt.module import Module


class DummyModule(Module):
    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass

    def entity(self, entity_type: str, field: str, value: str) -> object:
        if value == "MISSING":
            raise EntityNotFoundError("Entity with field value MISSING is never found by dummy module")
        if value == "DUPLICATE":
            raise DuplicateEntitiesError("Entity with field value DUPLICATE is allways found twice by dummy module")
        entity = super().entity(entity_type=entity_type, field=field, value=value)
        return entity
