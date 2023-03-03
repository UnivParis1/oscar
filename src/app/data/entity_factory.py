from dataclasses import dataclass, make_dataclass, field


@dataclass
class EntityFactory:

    @classmethod
    def entity_class(cls, entity_type, prefilled_field: str = None, prefilled_value: str = None, source: str = None):
        if entity_type == 'structure':
            return make_dataclass('Structure', [
                ('source', str, field(default=source)),
                ('director', str, field(default=None)),
                ('director_email', str, field(default=None)),
                ('title', str, field(default=None)),
                ('acronym', str, field(default=prefilled_value if prefilled_field == 'acronym' else None)),
                ('address', str, field(default=None)),
                ('rnsr_id', str, field(default=prefilled_value if prefilled_field == 'code' else None)),
                ('url', str, field(default=None)),
                ('number', str, field(default=prefilled_value if prefilled_field == 'number' else None)),
            ], unsafe_hash=True)
        elif entity_type == 'error':
            return make_dataclass('Error', [
                ('source', str, field(default=source)),
                ('message', str, field(default=prefilled_value if prefilled_field == 'message' else None)),
            ], unsafe_hash=True)
        raise ValueError(f"Entity type {entity_type} not supported yet")
