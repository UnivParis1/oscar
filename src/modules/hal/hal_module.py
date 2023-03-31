import re
from typing import Iterator

import requests
import pandas as pd

from app.module_mgmt.exceptions import EntityNotFoundError, DuplicateEntitiesError
from app.module_mgmt.module import Module


class HalModule(Module):
    HAL_QUERY_TIMEOUT = 60

    HAL_FIELDS = ['docid', 'type_s', 'acronym_s', 'parentAcronym_s', 'address_s', 'name_s', 'label_s', 'valid_s',
                  'code_s',
                  'rnsr_s', 'idref_s', 'code_s', 'updateDate_s', 'url_s']
    HAL_QUERY = f"https://api.archives-ouvertes.fr/ref/structure?" \
                f"q=parentDocid_i:7550" \
                f"&rows=1000" \
                f"&fq=(type_s:laboratory AND valid_s:(VALID))" \
                f"&wt=json" \
                f"&fl={','.join(HAL_FIELDS)}"

    CONVERSION_TABLE = {
        'rnsr_s': 'rnsr_id',
        'name_s': 'title',
        'acronym_s': 'acronym',
        'address_s': 'address',
        'url_s': 'url',
        'code_s': 'number'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aurehal_data = self._get_hal_research_structures()

    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass

    def entity(self, entity_type: str, field: str, value: str) -> object:
        assert field in ['acronym', 'code', 'number', 'title']
        entity = super().entity(entity_type=entity_type, field=field, value=value)
        hal_field_name = None
        if field == 'acronym':
            hal_field_name = "acronym_s"
        elif field == 'code':
            hal_field_name = "rnsr_s"
        elif field == 'number':
            hal_field_name = "code_s"
        elif field == 'title':
            hal_field_name = "name_s"
        assert hal_field_name is not None, f"Hal data request failure : unauthorized field {field}"
        data = self._extract_by_field("HAL", hal_field_name, value)
        for key in data.index:
            if key not in self.CONVERSION_TABLE:
                continue
            val = data[key][0] if isinstance(data[key], list) and len(data[key]) > 0 else data[key]
            setattr(entity, self.CONVERSION_TABLE[key], val)
        return entity

    def _get_hal_research_structures(self):
        json_data = requests.get(self.HAL_QUERY, timeout=self.HAL_QUERY_TIMEOUT).json()
        return pd.DataFrame(json_data['response']['docs'])

    def _extract_by_field(self, origin, column, value):
        filtered_data = pd.DataFrame.copy(self.aurehal_data)
        datatype = type(filtered_data[column].dropna().values[0])
        value = value.replace('*', '.*')
        if datatype == list:
            filtered_data = filtered_data.loc[
                filtered_data[column].str.join(' ').str.contains(f"^{value}$", regex=True, na=False)]
        else:
            filtered_data = filtered_data.loc[
                filtered_data[column].str.contains(f"^{value}$", regex=True, na=False, flags=re.IGNORECASE)]
        if filtered_data.shape[0] == 0:
            raise EntityNotFoundError("Non trouvé {origin} : {value}")
        if filtered_data.shape[0] > 1:
            values = ", ".join(filtered_data[column])
            raise DuplicateEntitiesError(f"Résultats multiples {origin} : {values}")
        return filtered_data.iloc(0)[0]
