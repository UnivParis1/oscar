from dataclasses import dataclass, make_dataclass, field


@dataclass
class EntityFactory:

    @classmethod
    def build_entity(cls, entity_type, prefilled_field: str, prefilled_value: str, source: str):
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
