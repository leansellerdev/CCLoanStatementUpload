import os
import subprocess

import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from loguru import logger

from settings import DEBUG, RESULTS_PATH


class Browser:
    def __init__(self) -> None:
        self.logger = logger

        self.options = self.__options
        self.chrome_version = self.__get_chrome_version

    @property
    def __options(self) -> uc.ChromeOptions:
        self.logger.debug("Setting options")
        options = uc.ChromeOptions()

        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')

        prefs = {
            "download.default_directory": str(RESULTS_PATH),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }

        options.add_experimental_option("prefs", prefs)

        # user_data_dir = r'C:\Users\96514502\AppData\Local\Google\Chrome\MySeleniumProfile'
        # options.add_argument("--profile-directory=MySeleniumProfile")
        # options.add_argument(f"--user-data-dir={user_data_dir}")

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
    def __get_chrome_version(self) -> int:
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

        self.logger.debug(f"Chrome version: {version}")
        return int(version.split(".")[0])

    @staticmethod
    def action_chain(driver: uc.Chrome) -> ActionChains:
        return ActionChains(driver)

    @staticmethod
    def wait(driver: uc.Chrome, wait_time: int) -> WebDriverWait:
        return WebDriverWait(driver, wait_time)
