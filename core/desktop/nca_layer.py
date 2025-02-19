from pywinauto import Application, ElementNotFoundError, WindowSpecification, keyboard, WindowNotFoundError
from pywinauto.application import ProcessNotFoundError

from loguru import logger

from core.utils import Logger, Config

from settings import nca_layer_path, open_jdk_path, KEY_PATH


class Desktop:
    def __init__(self) -> None:
        self.logger = logger
        self.app = Application()

    def _check_if_started(self, path) -> bool:
        try:
            self.app.connect(path=path)
            return True
        except ProcessNotFoundError:
            return False

    def set_window_focus(self, app_path: str,  title: str) -> WindowSpecification | None:
        if not self._check_if_started(app_path):
            self.logger.error(f"Process not started: {app_path.split('/')[-1]}")
            return

        self.app.connect(path=app_path)
        window = self.app.window(title=title)

        try:
            window.set_focus()
            return window
        except ElementNotFoundError:
            self.logger.error(f"Element not found: {title}")

class NCALayer(Desktop):
    def __init__(self) -> None:
        super().__init__()

        self.config = Config()

    def start(self) -> None:
        if not self._check_if_started(nca_layer_path):
            self.app.start(nca_layer_path)
            self.logger.info("NCALayer запущен.")

            return

        self.logger.warning("NCALayer уже запущен!")

    def choose_key(self):
        window = self.set_window_focus(open_jdk_path, 'Открыть файл')

        if not window:
            self.logger.error("Окно не активно")
            raise WindowNotFoundError

        keyboard.send_keys(str(KEY_PATH), pause=0)
        keyboard.send_keys('{ENTER}')

        window = self.set_window_focus(open_jdk_path, 'Формирование ЭЦП в формате XML')

        if not window:
            self.logger.error("Окно не активно")
            raise WindowNotFoundError

        keyboard.send_keys(self.config['password'], pause=0)
        keyboard.send_keys('{ENTER 2}', pause=1)


if __name__ == '__main__':
    nca = NCALayer()
    nca.choose_key()
    # time.sleep(600)
