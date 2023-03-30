from unittest.mock import patch

import pytest

from app.module_mgmt.exceptions import ConnectionFailureError, NotSupportedRequestError
from app.module_mgmt.module_manager import ModuleManager
from modules.ldap.ldap_module import LdapModule


class TestLdapModule:

    def test_wrong_config(self):
        ldap_module = self._init_ldap_module(conf_dir="conf/test_ldap_module_wrong_conf")
        with pytest.raises(ConnectionFailureError):
            ldap_module.entity("structure", "acronym", "CRI")

    def test_cri_title(self):
        ldap_module = self._init_ldap_module()
        with patch.object(LdapModule, '_get_ldap_research_structure',
                          return_value=self._cri_row()):
            entity = ldap_module.entity("structure", "acronym", "CRI")
            assert entity.title == 'Centre de recherche en informatique', "Entity title is 'Centre de recherche en informatique'"

    def test_cri_number(self):
        ldap_module = self._init_ldap_module()
        with patch.object(LdapModule, '_get_ldap_research_structure',
                          return_value=self._cri_row()):
            entity = ldap_module.entity("structure", "acronym", "CRI")
            assert entity.number == 'UR 1445', "Entity number is 'UR 1445'"

    def test_cri_address(self):
        ldap_module = self._init_ldap_module()
        with patch.object(LdapModule, '_get_ldap_research_structure',
                          return_value=self._cri_row()):
            entity = ldap_module.entity("structure", "acronym", "CRI")
            assert entity.address == 'Centre Pierre Mendès France\n90 RUE DE TOLBIAC\n75634 PARIS CEDEX 13\nFrance', "Entity address is 'Centre Pierre Mendès France\n90 RUE DE TOLBIAC\n75634 PARIS CEDEX 13\nFrance'"

    def test_cri_url(self):
        ldap_module = self._init_ldap_module()
        with patch.object(LdapModule, '_get_ldap_research_structure',
                          return_value=self._cri_row()):
            entity = ldap_module.entity("structure", "acronym", "CRI")
            assert entity.url == 'http://crinfo.univ-paris1.fr', "Entity website URL is 'http://crinfo.univ-paris1.fr'"
            

    def test_query_ldap_by_code_not_supported(self):
        ldap_module = self._init_ldap_module(conf_dir="conf/test_ldap_module_wrong_conf")
        with pytest.raises(NotSupportedRequestError):
            ldap_module.entity("structure", "code", "12345")

    @staticmethod
    def _cri_row() -> list[tuple]:
        return [('supannCodeEntite=U272,ou=structures,dc=univ-paris1,dc=fr', {'supannCodeEntite': [b'U272'],
                                                                              'objectClass': [b'organizationalUnit',
                                                                                              b'supannEntite',
                                                                                              b'up1Structure'],
                                                                              'labeledURI': [
                                                                                  b'http://crinfo.univ-paris1.fr'],
                                                                              'businessCategory': [b'research'],
                                                                              'supannCodeEntiteParent': [b'UR27'],
                                                                              'supannTypeEntite': [b'{SUPANN}S312'],
                                                                              'supannRefId': [b'{APOGEE.EQR}EA1445',
                                                                                              b'{SIHAM.UO}UR272_4'],
                                                                              'postalAddress': [
                                                                                  b'Centre Pierre Mend\xc3\xa8s France$90 RUE DE TOLBIAC$75634 PARIS CEDEX 13$France'],
                                                                              'telephoneNumber': [b'+33 1 44 07 80 00'],
                                                                              'ou': [b'UR 1445 - CRI'], 'description': [
                b'CRI\xc2\xa0: Centre de recherche en informatique (UR 1445)']})]

    @staticmethod
    def _init_ldap_module(conf_dir="conf/test_ldap_module_conf") -> LdapModule:
        module_manager = ModuleManager(conf_dir)
        for _ in module_manager.init_iterator(error_log_fn=print, success_log_fn=print):
            pass
        return module_manager.modules['ldap']
