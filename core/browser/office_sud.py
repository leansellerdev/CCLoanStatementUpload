import time

import undetected_chromedriver as uc
from pywinauto import keyboard
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, NoSuchAttributeException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from core.browser import Browser
from core.desktop import NCALayer
from settings import CASE_DIR


class OfficeSud(Browser):
    CASE_TYPE = 'CIVIL'
    INSTANCE = 'FIRSTINSTANCE'
    DOC_TYPE = '3'
    CAT_GROUP = '2'
    CAT = '28'
    STATEMENT_CHARACTER = '1'
    DISCTRICT = '3'
    COURT = '20'

    ORG_BIN = '151040016751'
    ORG_ADDRESS = 'Муратбаева 180 офис 404'

    KBK = '2'

    def __init__(self):
        super().__init__()

        self._BASE_URL = 'https://office.sud.kz/new/'
        self._SUD_URL = self._BASE_URL + 'index.xhtml'
        self._STATEMENT_PAGE = self._BASE_URL + '/form/send/index.xhtml'

        self.nca_layer = NCALayer()
        self.driver = uc.Chrome(version_main=self.chrome_version, options=self.options)

    def scroll_down(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

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

        select_button = self.wait(self.driver, 60).until(
            ec.presence_of_element_located((By.CSS_SELECTOR,
                                           '[onclick="showLoader(); selectSignType(); return false;"]'))
        )

        select_button.click()

    def login_via_key(self) -> None:
        self.nca_layer.start()

        self._get_url()
        self._change_language()

        time.sleep(3)

        self.__select_eds()

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

        # Выбираем опции подачи иска
        self.__select_options()

        self.scroll_down()
        time.sleep(3)

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
        district.click()
        time.sleep(5)
        district.click()

        district_select = Select(district)
        district_select.select_by_value(self.DISCTRICT)

    def __select_court(self) -> None:
        court = self.driver.find_element(By.ID, 'j_idt39:j_idt41:j_idt44:edit-court')

        court_select = Select(court)
        court_select.select_by_value(self.COURT)

    def set_participant_type(self, participant_type=None) -> None:
        type_ = self.driver.find_element(By.ID, 'j_idt173:pp-type')
        type_select = Select(type_)

        if participant_type:
            type_select.select_by_value('false')
        else:
            type_select.select_by_value('true')
        time.sleep(2)

        proc_side = self.driver.find_element(By.ID, 'j_idt173:pp-side')
        proc_side_select = Select(proc_side)

        if participant_type:
            proc_side_select.select_by_value('2')
        else:
            proc_side_select.select_by_value('1')
        time.sleep(2)

        goto_button = self.driver.find_element(By.ID, 'j_idt173:j_idt193')
        goto_button.click()

    def fill_requisites(self) -> None:
        bin_field = self.driver.find_element(By.ID, 'j_idt199:org-bin')
        bin_field.send_keys(self.ORG_BIN)
        bin_field.click()

        search_button = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="j_idt199:jurModalDialogPanel"]/div/div[1]/table/tbody/tr[4]/td[2]/div/span[1]')
        ))
        search_button.click()

        address_field = self.driver.find_element(By.ID, 'j_idt199:org-factAddress')
        address_field.send_keys(self.ORG_ADDRESS)

        requisites_field = self.driver.find_element(By.ID, 'j_idt199:org-bankDetails')
        requisites_field.send_keys('1')
        time.sleep(1)

        save_button = self.driver.find_element(By.ID, 'j_idt199:j_idt261')
        save_button.click()

    def fill_fiz_info(self, iin: str) -> None:
        iin_field = self.driver.find_element(By.ID, 'j_idt266:person-iin')
        iin_field.send_keys(iin)

        search_button = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="j_idt266:fizModalDialogPanel"]/div/div[1]/table/tbody/tr[3]/td[2]/div/span[1]')
        ))
        search_button.click()
        time.sleep(1)

        save_button = self.wait(self.driver, 60).until(ec.element_to_be_clickable(
            (By.ID, 'j_idt266:j_idt318')
        ))
        save_button.click()

    def add_participant(self, iin=None) -> None:
        add_participant_button = self.driver.find_element(By.CSS_SELECTOR, '[onclick="renderAddPersonModalDialog()"]')
        add_participant_button.click()
        time.sleep(2)

        self.wait(self.driver, 5).until(ec.presence_of_element_located(
            (By.ID, 'j_idt173')
        ))

        self.set_participant_type(iin)
        time.sleep(2)

        if not iin:
            self.fill_requisites()
        else:
            self.fill_fiz_info(iin)

    def fill_data(self) -> None:
        # Выбираем группу категорий
        self.__select_category_group()
        time.sleep(5)

        # Выбираем категорию
        self.__select_category()
        time.sleep(5)

        # Выбираем характер иска
        self.__select_statement_character()
        time.sleep(10)

        self.scroll_down()

        # Выбираем область
        self.__select_district()
        time.sleep(5)

        # Выбираем суд
        self.__select_court()
        time.sleep(5)

    def fill_payment(self, statement_sum: str) -> None:
        kbk = self.driver.find_element(By.ID, 'j_idt37:j_idt39:j_idt42:selectKbk')
        kbk_select = Select(kbk)

        kbk_select.select_by_value(self.KBK)
        time.sleep(5)

        sum_field = self.driver.find_element(By.ID, 'j_idt37:j_idt39:j_idt42:personTableRows:0:edit-totalSum')
        sum_field.clear()
        sum_field.send_keys(statement_sum)

        state_duty_field = self.driver.find_element(By.ID, 'j_idt37:j_idt39:j_idt42:personTableRows:0:edit-duty')
        state_duty_field.clear()
        state_duty_field.send_keys(int(statement_sum) * 0.03)
        time.sleep(5)

    def upload_payment(self, input_path: str, file_path: str) -> None:
        file_input = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.ID, input_path)
        ))
        file_input.click()
        time.sleep(2)

        keyboard.send_keys(str(file_path), pause=0)
        keyboard.send_keys('{ENTER}')
        time.sleep(2)

    def upload_file(self, input_path: str, file_path: str) -> None:
        file_input = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, input_path)
        ))
        file_input.click()
        time.sleep(2)

        keyboard.send_keys(str(file_path), pause=0)
        keyboard.send_keys('{ENTER}')
        time.sleep(2)

    def fill_statement_requirements(self):
        base_req = 'ИСКОВОЕ ЗАЯВЛЕНИЕ о взыскании задолженности по договору о предоставлении микрокредита'
        for _ in range(15):
            base_req += '1'

        text_area = self.driver.find_element(By.ID, 'j_idt37:j_idt39:j_idt42:edit-plaint-description')
        text_area.send_keys(base_req)
        time.sleep(2)

        text_area = self.driver.find_element(By.ID, 'j_idt37:j_idt39:j_idt42:edit-plaint-additional')
        text_area.send_keys(base_req)
        time.sleep(2)

    def fill_data_page(self, iin: str) -> None:
        self.fill_data()

        self.add_participant()
        time.sleep(5)

        self.add_participant(iin)
        time.sleep(5)

        next_page_button = self.driver.find_element(By.XPATH,
                                                    '//*[@id="j_idt39:j_idt41:j_idt44:button-panel"]/a[2]')
        next_page_button.click()
        time.sleep(5)

    def payment_page(self, statement_sum: str, iin: str) -> None:
        case_folder = CASE_DIR / iin

        payment_upload_path = 'j_idt37:j_idt39:j_idt42:personTableRows:0:j_idt126'
        self.fill_payment(statement_sum)

        # TODO: сделать загрузку чека
        self.upload_payment(payment_upload_path, case_folder / 'doc_6.pdf')
        time.sleep(5)

        next_page_button = self.driver.find_element(By.XPATH,
                                                    '//*[@id="j_idt37:j_idt39:j_idt42"]/div[2]/div[1]/div[2]/div/a[2]')
        next_page_button.click()
        time.sleep(5)

    def upload_files_page(self, iin: str) -> None:
        case_folder = CASE_DIR / iin

        statement_path = case_folder / f'Исковое_Заявление_{iin}.docx'
        doc_6_path = case_folder / 'doc_6.pdf'
        licence_path = case_folder / 'licence.pdf'
        hod_path = case_folder / 'Ходатайство_об_отмене_упр_производства.docx'

        dogovor_path = [file for file in case_folder.iterdir() if 'dogovor' in str(file)][0]
        dolg_path = [file for file in case_folder.iterdir() if 'dolg' in str(file)][0]
        uved_path = [file for file in case_folder.iterdir() if 'uvedomlenie' in str(file)][0]

        docs = [doc_6_path, licence_path, hod_path, dogovor_path, dolg_path, uved_path]

        self.upload_file('[value="Загрузить иск"]', statement_path)

        for i, doc in enumerate(docs):
            self.upload_file('[value="Прикрепить файл"]', doc)

            self.wait(self.driver, 60).until(ec.visibility_of_element_located(
                (By.CSS_SELECTOR, '[value="Прикрепить файл"]')
            ))

        self.fill_statement_requirements()

        next_page_button = self.driver.find_element(By.XPATH,
                                                    '//*[@id="j_idt37:j_idt39:j_idt42"]/div[2]/div[1]/div/a[2]')
        next_page_button.click()
        time.sleep(5)

    def sign_statement_page(self) -> None:
        choose_eds_button = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, '[onclick="showLoader(); selectSignType(); return false;"]')
        ))

        choose_eds_button.click()

        self.nca_layer.choose_key()
        time.sleep(5)

    def result_page(self) -> None:
        safe_talon_button = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.ID, 'j_idt37:j_idt39:j_idt42:j_idt46')
        ))

        safe_talon_button.click()
        time.sleep(5)

    def process(self, iin: str, statement_sum: str) -> None:
        self.logger.info("Логинимся на сайте")
        self.login_via_key()

        self.logger.info("Выбираем опции иска")
        self.choose_options()

        self.logger.info("Заполняем данные иска")
        self.fill_data_page(iin)

        self.logger.info("Указываем данные платежа + загружаем чек")
        self.payment_page(statement_sum, iin)

        self.logger.info("Загружаем файлы")
        self.upload_files_page(iin)

        self.logger.info("Подписываем подачу иска")
        self.sign_statement_page()

        self.logger.info("Скачиваем итоговый файл")
        self.result_page()


if __name__ == '__main__':
    try:
        uploader = OfficeSud()
        uploader.process('940928451011', "60000")
        time.sleep(6000)
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted!")
