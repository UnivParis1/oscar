import re
import time
from typing import Iterator

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bleach.sanitizer import Cleaner

from app.module_mgmt.exceptions import EntityNotFoundError
from app.module_mgmt.module import Module

SEARCH_FORM_URL = 'https://appliweb.dgri.education.fr/rnsr/ChoixCriteres.jsp?PUBLIC=OK'


class RnsrModule(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaner = Cleaner(tags=[], attributes={}, protocols=[], strip=True, strip_comments=True,
                               filters=None)

    def values_for(self, entity_type: str, field: str) -> Iterator[str]:
        pass

    rnsr_directors_regex = re.compile(r'^\s*Directeur - (.+) à partir du .+ \( (.+@.+) \)<br>\s*$')
    rnsr_title_regex = re.compile(r'^([A-Z0-9]+)\s*:\s*(.+)$')
    rnsr_intitule_regex = re.compile(r'^\s*([A-Z0-9a-z]+\s)?([A-Z].+)\s*$')

    def entity(self, entity_type: str, field: str, value: str) -> object:
        assert field in ['acronym', 'code', 'number', 'title']
        entity = super().entity(entity_type=entity_type, field=field, value=value)
        acronym = value if field == 'acronym' else None
        rnsr_code = value if field == 'code' else None
        data = self._get_research_structure_data(rnsr_code=rnsr_code, acronym=acronym)
        for key in data:
            setattr(entity, key, data[key])
        return entity

    def _get_research_structure_data(self, rnsr_code=None, acronym=None):
        driver = self._get_web_driver()
        driver.get(SEARCH_FORM_URL)
        self._execute_query(driver, acronym, rnsr_code)
        acronym, number, title = self._extract_title_and_identifiers(acronym, driver)
        director, director_email = self._extract_directors(driver)
        address = self._extract_address(driver)
        return {'director': director,
                'director_email': director_email,
                'title': title,
                'acronym': acronym,
                'rnsr_id': number,
                'address': address}

    def _extract_address(self, driver):
        try:
            raw_adresses = driver.find_element(By.XPATH,
                                               '//b[text()[normalize-space() = "Adresse"]]/..').get_attribute(
                'innerHTML')
            lines = list(map(lambda s: s.replace('\t', ''), raw_adresses.splitlines()))
            raw = self.cleaner.clean(' '.join(lines))
            raw = re.sub(r'Adresse\s+', '', raw)
            address = re.sub(r'(\s+|&nbsp;)', ' ', raw)
        except selenium.common.exceptions.NoSuchElementException:
            address = None
        return address

    def _extract_directors(self, driver):
        try:
            raw_directors = driver.find_element(By.XPATH,
                                                '//h2[text()[normalize-space() = "Responsable(s)"]]/..').get_attribute(
                'innerHTML')
            lines = list(map(lambda s: s.replace('\t', ''), raw_directors.splitlines()))
            values = list(map(self.rnsr_directors_regex.match, lines))
            not_none = (el for el in values if el is not None)
            value = next(not_none, None)
            director = None if value is None else value.group(1)
            director_email = None if value is None else value.group(2)
        except selenium.common.exceptions.NoSuchElementException:
            director = None
            director_email = None
        return director, director_email

    def _extract_title_and_identifiers(self, acronym, driver):
        try:
            title = driver.find_element(By.XPATH, '//h2').text.split('\n')[0]
        except selenium.common.exceptions.NoSuchElementException:
            raise EntityNotFoundError(f"Non trouvé RNSR : {acronym}")
        match_title = self.rnsr_title_regex.match(title)
        num = None if match_title is None else match_title.group(1)
        name = None if match_title is None else match_title.group(2)
        match_name = self.rnsr_intitule_regex.match(name)
        acronym = None if match_name is None else match_name.group(1)
        title = None if match_name is None else match_name.group(2)
        return acronym, num, title

    def _execute_query(self, driver, acronym, rnsr_id):
        if rnsr_id is not None:
            driver.find_element(By.XPATH, '//input[@name="NUM_NAT_STRUCT"]').send_keys(rnsr_id)
        elif acronym is not None:
            driver.find_element(By.XPATH, '//input[@name="STRUCT.LIBELLE"]').send_keys(acronym)
        button = driver.find_element(By.XPATH, '//input[@name="RECHERCHE"]')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of(button))
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)

    def _get_web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        return driver
