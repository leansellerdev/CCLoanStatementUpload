import time

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, NoSuchAttributeException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from core.browser import Browser
from core.desktop import NCALayer


class OfficeSud(Browser):
    CASE_TYPE = 'CIVIL'
    INSTANCE = 'FIRSTINSTANCE'
    DOC_TYPE = '3'
    CAT_GROUP = '2'
    CAT = '28'
    STATEMENT_CHARACTER = '1'
    DISCTRICT = '3'
    COURT = '20'

    def __init__(self):
        super().__init__()

        self._BASE_URL = 'https://office.sud.kz/new/'
        self._SUD_URL = self._BASE_URL + 'index.xhtml'
        self._STATEMENT_PAGE = self._BASE_URL + '/form/send/index.xhtml'

        self.nca_layer = NCALayer()

    def _get_url(self) -> None:
        self.logger.info("Заходим на сайт")
        self.driver.maximize_window()
        self.driver.get(self._SUD_URL)

    def _change_language(self, lang: str = 'rus') -> None:
        language_changed = False

        if lang == 'rus':
            language = 'русский'
            self.logger.info("Меняем язык отображения на русский")

            button = self.driver.find_element(By.CSS_SELECTOR,
                                              '[onclick="selectLanguageRu(window.location); return false;"]')
        else:
            language = 'казахский'
            self.logger.info("Меняем язык отображения на казахский")

            button = self.driver.find_element(By.CSS_SELECTOR,
                                              '[onclick="selectLanguageKk(window.location); return false;"]')
        while not language_changed:
            try:
                button.click()
            except NoSuchElementException:
                pass
            else:
                try:
                    button.get_attribute('class')
                except NoSuchAttributeException:
                    pass
                else:
                    language_changed = True

        self.logger.info(f"Язык изменен на {language}")

    def __select_eds(self) -> None:
        tab_eds = self.driver.find_element(By.ID, 'tab-eds')
        tab_eds.click()

        select_button = self.wait(self.driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR,
                                           '[onclick="showLoader(); selectSignType(); return false;"]'))
        )

        select_button.click()

    def login_via_key(self) -> None:
        self._get_url()
        self._change_language()

        time.sleep(3)

        self.__select_eds()

        self.nca_layer.start()
        self.nca_layer.choose_key()

        self.wait(self.driver, 60).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '[href="/new/form/send/index.xhtml"]')
            )
        )

    def __select_case_type(self) -> None:
        case_type = self.driver.find_element(By.ID, 'j_idt36:j_idt38:j_idt39:case-type')
        case_type_select = Select(case_type)

        case_type_select.select_by_value(self.CASE_TYPE)

    def __select_instance(self) -> None:
        instance = self.driver.find_element(By.ID, 'j_idt36:j_idt38:j_idt39:instance')
        instance_type_select = Select(instance)

        instance_type_select.select_by_value(self.INSTANCE)

    def __select_doc_type(self) -> None:
        doct_type = self.driver.find_element(By.ID, 'j_idt36:j_idt38:j_idt39:request')
        doct_type_select = Select(doct_type)

        doct_type_select.select_by_value(self.DOC_TYPE)

    def __select_options(self) -> None:
        # Выбираем тип производства
        self.__select_case_type()

        # Выбираем инстанцию
        self.__select_instance()
        time.sleep(10)

        # Выбираем тип документа
        self.__select_doc_type()

    def choose_options(self) -> None:
        current_page = self.driver.current_url

        if current_page != self._STATEMENT_PAGE:
            self.driver.get(self._STATEMENT_PAGE)
        time.sleep(5)

        # TODO: Refresh page in case of error
        # Выбираем опции подачи иска
        self.__select_options()

        # Подтверждаем настройки
        send_button = self.driver.find_element(By.CSS_SELECTOR, '[onclick="sendRequest()"]')
        send_button.click()

    def __select_category_group(self) -> None:
        category_group = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-categoryGroup')

        category_group_select = Select(category_group)
        category_group_select.select_by_value(self.CAT_GROUP)

    def __select_category(self) -> None:
        category = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-category')

        category_select = Select(category)
        category_select.select_by_value(self.CAT)

    def __select_statement_character(self) -> None:
        statement_character = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-character')

        statement_character_select = Select(statement_character)
        statement_character_select.select_by_value(self.STATEMENT_CHARACTER)

    def __select_district(self) -> None:
        district = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-district')

        district_select = Select(district)
        district_select.select_by_value(self.DISCTRICT)

    def __select_court(self) -> None:
        court = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-court')

        court_select = Select(court)
        court_select.select_by_value(self.COURT)

    def fill_data(self) -> None:
        # Выбираем группу категорий
        self.__select_category_group()
        time.sleep(5)

        # Выбираем категорию
        self.__select_category()
        time.sleep(5)

        # Выбираем характер иска
        self.__select_options()
        time.sleep(5)

        # Выбираем район
        self.__select_statement_character()
        time.sleep(5)

        # Выбираем суд
        self.__select_court()


if __name__ == '__main__':
    try:
        uploader = OfficeSud()
        uploader.login_via_key()
        uploader.choose_options()
        uploader.fill_data()
        time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted!")
