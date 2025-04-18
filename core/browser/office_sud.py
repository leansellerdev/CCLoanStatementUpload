import os
import shutil
import time

import undetected_chromedriver as uc
from pywinauto import keyboard
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, NoSuchAttributeException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from core.browser import Browser
from core.desktop import NCALayer

from core.telegram import send_payment_info

from settings import CASE_DIR, RESULTS_PATH, RESULTS_DIR


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

    def __init__(self, logger):
        super().__init__()
        self.logger = logger

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
        self.driver.set_page_load_timeout(120)
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
        case_type = self.driver.find_element(By.XPATH, '//select[contains(@id, "case-type")]')
        case_type_select = Select(case_type)

        case_type_select.select_by_value(self.CASE_TYPE)

    def __select_instance(self) -> None:
        instance = self.driver.find_element(By.XPATH, '//select[contains(@id, "instance")]')
        instance_type_select = Select(instance)

        instance_type_select.select_by_value(self.INSTANCE)

    def __select_doc_type(self) -> None:
        doct_type = self.driver.find_element(By.XPATH, '//select[contains(@id, "request")]')
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
        category_group = self.wait(self.driver, 15).until(ec.presence_of_element_located(
            (By.XPATH, '//select[contains(@id, "edit-categoryGroup")]')
        ))

        category_group_select = Select(category_group)
        category_group_select.select_by_value(self.CAT_GROUP)

    def __select_category(self) -> None:
        category = self.driver.find_elements(By.XPATH, '//select[contains(@id, "edit-category")]')[-1]

        category_select = Select(category)
        category_select.select_by_value(self.CAT)

    def __select_statement_character(self) -> None:
        statement_character = self.driver.find_element(By.XPATH, '//select[contains(@id, "edit-character")]')

        statement_character_select = Select(statement_character)
        statement_character_select.select_by_value(self.STATEMENT_CHARACTER)

    def __select_district(self) -> None:
        district = self.driver.find_element(By.XPATH, '//select[contains(@id, "edit-district")]')
        district.click()
        time.sleep(5)
        district.click()

        district_select = Select(district)
        district_select.select_by_value(self.DISCTRICT)

    def __select_court(self) -> None:
        court = self.driver.find_element(By.XPATH, '//select[contains(@id, "edit-court")]')

        court_select = Select(court)
        court_select.select_by_value(self.COURT)

    def set_participant_type(self, participant_type=None) -> None:
        type_ = self.driver.find_element(By.XPATH, '//select[contains(@id, "pp-type")]')
        type_select = Select(type_)

        if participant_type:
            type_select.select_by_value('false')
        else:
            type_select.select_by_value('true')
        time.sleep(2)

        proc_side = self.driver.find_element(By.XPATH, '//select[contains(@id, "pp-side")]')
        proc_side_select = Select(proc_side)

        if participant_type:
            proc_side_select.select_by_value('2')
        else:
            proc_side_select.select_by_value('1')
        time.sleep(2)

        goto_button = self.driver.find_elements(By.XPATH,
                                               '//input[contains(@value, "Далее")]')[0]
        goto_button.click()

    def fill_requisites(self) -> None:
        bin_field = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//input[contains(@id, "org-bin")]')
        ))
        bin_field.send_keys(self.ORG_BIN)
        bin_field.click()

        search_button = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//span[contains(@onclick, "fillOrgData")]')
        ))
        search_button.click()

        address_field = self.driver.find_element(By.XPATH, '//input[contains(@id, "org-factAddress")]')
        address_field.send_keys(self.ORG_ADDRESS)

        requisites_field = self.driver.find_element(By.XPATH, '//input[contains(@id, "org-bankDetails")]')
        requisites_field.send_keys('1')
        time.sleep(1)

        save_button = self.driver.find_element(By.XPATH, '//input[contains(@value, "Сохранить") and contains(@class, "btn btn-primary")]')

        clicked = False

        while not clicked:
            try:
                save_button.click()
            except (ElementNotInteractableException, ElementClickInterceptedException):
                pass
            else:
                clicked = True


    def fill_fiz_info(self, iin: str) -> None:
        iin_field = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//input[contains(@id, "person-iin")]')
        ))
        iin_field.send_keys(iin)

        search_button = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//span[contains(@onclick, "fillPersonData")]')
        ))
        search_button.click()
        time.sleep(1)

        save_button = self.wait(self.driver, 60).until(ec.element_to_be_clickable(
            (By.XPATH, '//input[contains(@value, "Сохранить") and contains(@class, "button button-primary")]')
        ))
        clicked = False

        while not clicked:
            try:
                save_button.click()
            except ElementClickInterceptedException:
                pass
            else:
                clicked = True

    def add_participant(self, iin=None) -> None:
        add_participant_button = self.driver.find_element(By.CSS_SELECTOR, '[onclick="renderAddPersonModalDialog()"]')
        self.wait(self.driver, 20).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '[onclick="renderAddPersonModalDialog()"]')
        ))
        add_participant_button.click()
        time.sleep(2)

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

    def fill_payment(self, statement_sum: str, state_duty: str) -> None:
        kbk = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.XPATH, '//select[contains(@id, "selectKbk")]')
        ))
        kbk_select = Select(kbk)

        kbk_select.select_by_value(self.KBK)
        time.sleep(5)

        sum_field = self.driver.find_element(By.XPATH, '//input[contains(@id, "edit-totalSum")]')
        sum_field.clear()
        sum_field.send_keys(statement_sum)

        state_duty_field = self.driver.find_element(By.XPATH, '//input[contains(@id, "edit-duty")]')
        state_duty_field.clear()
        state_duty_field.send_keys(state_duty)
        time.sleep(5)

    def online_payment(self) -> None:
        check_box = self.driver.find_element(By.XPATH, '//input[contains(@id, "isonline-payment")]')
        check_box.click()

        online_payment_button = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, '[onclick="fillHideFields(); doPay1(); return false;"]')
        ))
        online_payment_button.click()

    def get_payment_code(self) -> str:
        payment_code = self.wait(self.driver, 10).until(ec.presence_of_element_located(
            (By.ID, 'ctl00_CPH1_payCodeValue')
        )).text

        return payment_code

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
        file_input = self.wait(self.driver, 60).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, input_path)
        ))
        self.wait(self.driver, 120).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, input_path)
        ))

        clicked = False

        while not clicked:
            try:
                file_input.click()
            except ElementClickInterceptedException:
                pass
            else:
                clicked = True

        time.sleep(2)

        keyboard.send_keys(str(file_path), pause=0)
        keyboard.send_keys('{ENTER}')
        time.sleep(3)

    def fill_statement_requirements(self):
        base_req = 'ИСКОВОЕ ЗАЯВЛЕНИЕ о взыскании задолженности по договору о предоставлении микрокредита'
        for _ in range(15):
            base_req += '1'

        text_area = self.driver.find_element(By.XPATH, '//textarea[contains(@id, "edit-plaint-description")]')
        text_area.send_keys(base_req)
        time.sleep(2)

        text_area = self.driver.find_element(By.XPATH, '//textarea[contains(@id, "edit-plaint-additional")]')
        text_area.send_keys(base_req)
        time.sleep(2)

    def fill_data_page(self, iin: str) -> None:
        self.fill_data()

        self.add_participant()
        time.sleep(5)

        self.add_participant(iin)
        time.sleep(5)

        next_page_button = self.driver.find_element(By.CSS_SELECTOR,
                                                    '[onclick="fillHideFields(); goNext(); return false;"]')
        next_page_button.click()
        time.sleep(5)

    def payment_page(self, statement_sum: str, state_duty: str) -> str:
        self.fill_payment(statement_sum, state_duty)

        self.online_payment()
        payment_code = self.get_payment_code()

        time.sleep(3)
        self.driver.back()

        check_box = self.driver.find_element(By.XPATH, '//input[contains(@id, "isonline-payment")]')
        # check_box = self.wait(self.driver, 60).until(ec.element_to_be_clickable(
        #     (By.XPATH, '//input[contains(@id, "ad")]')
        # ))
        clicked = False

        while not clicked:
            try:
                check_box.click()
            except ElementClickInterceptedException:
                pass
            else:
                clicked = True

        time.sleep(5)
        clicked = False

        while not clicked:
            try:
                check_box.click()
            except ElementClickInterceptedException:
                pass
            else:
                clicked = True

        check_status_button = self.wait(self.driver, 60).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, '[onclick="doCheckPayments(); return false;"]')
        ))
        check_status_button.click()
        time.sleep(5)

        next_page_button = self.driver.find_element(By.CSS_SELECTOR,
                                                    '[onclick="fillHideFields(); goToDocuments(); return false;"]')
        clicked = False
        while not clicked:
            try:
                next_page_button.click()
            except ElementClickInterceptedException:
                pass
            else:
                clicked = True

        time.sleep(5)

        return payment_code

    def upload_files_page(self, iin: str, paybox: str) -> None:
        case_folder = CASE_DIR / f'{iin}_{paybox}'

        statement_path = case_folder / f'Исковое_Заявление_{iin}.docx'
        doc_6_path = case_folder / 'Приказ_о_назначении_директора.pdf'
        licence_path = case_folder / 'Лицензия.pdf'
        hod_path = case_folder / 'Ходатайство_об_отмене_упр_производства.docx'
        yur_dogovor_path = case_folder / 'Договор_на_оказание_юридических_услуг.pdf'
        platezh_path = case_folder / f'{iin}_ПлатежПор.pdf'

        dogovor_path = [file for file in case_folder.iterdir() if 'Договор_о_предоставлении_микрокредита' in str(file)][0]
        dolg_path = [file for file in case_folder.iterdir() if 'Рассчет_задолженности' in str(file)][0]
        uved_path = [file for file in case_folder.iterdir() if 'Досудебная_претензия' in str(file)][0]

        docs = [doc_6_path, licence_path, hod_path, dogovor_path, dolg_path, uved_path, yur_dogovor_path, platezh_path]

        self.upload_file('[value="Загрузить иск"]', statement_path)

        for i, doc in enumerate(docs):
            self.upload_file('[value="Прикрепить файл"]', doc)

            self.wait(self.driver, 60).until(ec.visibility_of_element_located(
                (By.CSS_SELECTOR, '[value="Прикрепить файл"]')
            ))

        self.fill_statement_requirements()

        next_page_button = self.driver.find_element(By.CSS_SELECTOR,
                                                    '[onclick="goToSign(); return false;"]')
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
        safe_talon_button = self.wait(self.driver, 120).until(ec.presence_of_element_located(
            (By.XPATH, '//input[contains(@value, "Скачать талон об отправке")]')
        ))

        safe_talon_button.click()
        time.sleep(5)

    @staticmethod
    def move_result_notification(iin: str, paybox: str) -> None:
        files = os.listdir(RESULTS_PATH)
        paths = [os.path.join(RESULTS_PATH, filename) for filename in files]

        latest_file = max(paths, key=os.path.getctime)

        shutil.move(latest_file, CASE_DIR / f'{iin}_{paybox}' / 'уведомление_об_отправке.pdf')

    @staticmethod
    def move_result_when_done(iin: str, paybox: str) -> None:
        shutil.move(CASE_DIR / f'{iin}_{paybox}', RESULTS_DIR)

    def process(self, statement_info: dict) -> None:
        self.logger.info("Логинимся на сайте")
        self.login_via_key()

        self.logger.info("Выбираем опции иска")
        self.choose_options()

        self.logger.info("Заполняем данные иска")
        self.fill_data_page(statement_info.get('iin'))

        self.logger.info("Указываем данные платежа + берем идентификатор платежа")
        payment_code = self.payment_page(statement_info.get('final_summa'), statement_info.get('state_duty'))
        statement_info['payment_code'] = payment_code

        self.logger.info("Загружаем файлы")
        self.upload_files_page(statement_info.get('iin'), statement_info.get('paybox'))

        self.logger.info("Подписываем подачу иска")
        self.sign_statement_page()

        self.logger.info("Скачиваем итоговый файл")
        self.result_page()

        self.move_result_notification(statement_info.get('iin'), statement_info.get('paybox'))
        self.driver.close()

        notification_path = CASE_DIR / f"{statement_info.get('iin')}_{statement_info.get('paybox')}" / 'уведомление_об_отправке.pdf'

        send_payment_info(statement_info, notification_path)
        self.move_result_when_done(statement_info.get('iin'), statement_info.get('paybox'))
