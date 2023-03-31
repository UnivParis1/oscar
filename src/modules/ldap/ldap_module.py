import re
from typing import Iterator

import ldap
from prompt_toolkit import print_formatted_text, HTML

from app.module_mgmt.exceptions import EntityNotFoundError, DuplicateEntitiesError, ConnectionFailureError, \
    NotSupportedRequestError
from app.module_mgmt.module import Module


class LdapModule(Module):
    STRUCTURE_BRANCH = 'ou=structures,dc=univ-paris1,dc=fr'

    CONVERSION_TABLE = {
        'postalAddress': 'address',
        'labeledURI': 'url',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connexion = ldap.initialize(self.config['url'])

    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass

    def entity(self, entity_type: str, field: str, value: str) -> object:
        assert field in ['acronym', 'code', 'number', 'title']
        if field == "code":
            raise NotSupportedRequestError("L'annuaire LDAP : pas de code RNSR.")
        entity = super().entity(entity_type=entity_type, field=field, value=value)
        ldap_response = self._get_ldap_research_structure(field, value)
        num_results = len(ldap_response)
        if num_results == 0:
            raise EntityNotFoundError(f"Non trouvé {field} : {value}")
        if num_results > 1:
            raise DuplicateEntitiesError(f"Résultats multiples ({num_results}) {field} : {value}")
        data = ldap_response[0][1]
        for key in data:
            if key == 'ou':
                # expected [b'UR 1445 - CRI']
                value = data[key][0]
                values = list(map(lambda s: s.decode('utf-8').strip(), value.split(b'-')))
                if not len(values) == 2:
                    print_formatted_text(HTML(f"<red>Malformed ou field {value.decode('utf-8')}</red>"))
                    continue
                number, acronym = values
                setattr(entity, 'number', number)
                setattr(entity, 'acronym', acronym)
                continue
            if key == 'description':
                # expected [b'CRI\xc2\xa0: Centre de recherche en informatique (UR 1445)']
                value = data[key][0].decode('utf-8')
                match = re.search(r"^(.+)\s*:\s*(.+)\s*\((.+)\)$", value)
                if not len(match.groups()) == 3:
                    print_formatted_text(HTML(f"<red>Malformed description {value}</red>"))
                    continue
                acronym, title, number = match.groups()
                setattr(entity, 'number', number.strip())
                setattr(entity, 'title', title.strip())
                setattr(entity, 'acronym', acronym.strip())
                continue
            if key not in self.CONVERSION_TABLE:
                continue
            val = data[key][0] if isinstance(data[key], list) and len(data[key]) > 0 else data[key]
            if isinstance(val, bytes):
                val = val.decode('utf-8').replace('$', '\n')
            setattr(entity, self.CONVERSION_TABLE[key], val)
        return entity

    def _get_ldap_research_structure(self, field, value):
        query = None
        if field == 'acronym':
            query = f"ou=*{value}"
        elif field == 'number':
            query = f"supannRefId=*{value.replace(' ', '')}"
        elif field == 'title':
            query = f"description=*{value}*"
        assert query is not None, f"Ldap request failure : unauthorized field {field}"
        try:
            ldap_response = self.connexion.search_s(LdapModule.STRUCTURE_BRANCH,
                                                    ldap.SCOPE_SUBTREE,
                                                    query)
        except ldap.SERVER_DOWN as error:
            raise ConnectionFailureError("Connexion au LDAP impossible") from error
        except ldap.SIZELIMIT_EXCEEDED:
            raise DuplicateEntitiesError("Réponses LDAP en nombre excessif")
        return ldap_response
