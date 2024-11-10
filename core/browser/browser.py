import os
import subprocess

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from core.utils import Logger

from settings import DEBUG


class Browser:
    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__, to_file=False).set_logger()

        # self.options = self.__set_options
        self.chrome_version = self.__get_chrome_version

    @property
    def __options(self) -> Options:
        self.logger.info("Setting options")
        options = Options()

        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')

        options.add_argument("--width=device-width")
        options.add_argument("--initial-scale=1")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-notifications")
        options.add_argument(f"--user-agent={user_agent}")

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        if not DEBUG:
            options.add_argument("--headless")  # Запуск в headless режиме
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-translate")
            options.add_argument("--disable-web-resources")
            options.add_argument("--enable-logging")
            options.add_argument("--v=1")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--width=device-width")
            options.add_argument("--initial-scale=1")

        return options

    @property
    def __get_chrome_version(self) -> str:
        if os.name == 'nt':
            import winreg

            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version = winreg.QueryValueEx(reg_key, 'Version')[0]
        else:
            output = subprocess.check_output(["google-chrome", "--version"])
            try:
                version = output.decode("utf-8").split()[-1]
            except Exception as error:
                raise Exception(f"Ошибка при проверке версии браузера: {error}")

        self.logger.info(f"Chrome version: {version}")
        return version.split(".")[0]

    @staticmethod
    def action_chain(driver: uc.Chrome) -> ActionChains:
        return ActionChains(driver)

    @staticmethod
    def wait(driver: uc.Chrome, wait_time: int) -> WebDriverWait:
        return WebDriverWait(driver, wait_time)
