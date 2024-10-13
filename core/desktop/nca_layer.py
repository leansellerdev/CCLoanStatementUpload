from pywinauto import Application
from pywinauto.application import ProcessNotFoundError

from core.utils import Logger

from settings import nca_layer_path

class NCALayer:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__, to_file=False).set_logger()

        self.app = Application()

    def _check_if_started(self) -> bool:
        try:
            self.app.connect(path=nca_layer_path)
            return True
        except ProcessNotFoundError:
            return False

    def start(self) -> None:
        if not self._check_if_started():
            self.app.start(nca_layer_path)
            self.logger.info("NCALayer запущен.")

            return

        self.logger.warning("NCALayer уже запущен!")


if __name__ == '__main__':
    nca = NCALayer()
    nca.start()
