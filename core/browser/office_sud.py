import time

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from browser import Browser
from ..desktop import NCALayer



class OfficeSud(Browser):
    def __init__(self):
        super().__init__()

        self._SUD_URL = 'https://office.sud.kz/new/index.xhtml'
        self.driver = self.driver(keep_alive=False)

        self.nca_layer = NCALayer()

    def _get_url(self) -> None:
        self.logger.info("Заходим на сайт")
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
                language_changed = True

        self.logger.info(f"Язык изменен на {language}")

    def login_via_key(self) -> None:
        self._get_url()
        self._change_language()


if __name__ == '__main__':
    try:
        uploader = OfficeSud()
        uploader.login_via_key()
        time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted!")
