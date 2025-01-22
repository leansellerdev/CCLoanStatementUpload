import sys

from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.browser.office_sud import OfficeSud
from core.scanning import get_statement_sum, scan_folders

from core.utils.logger import Logger

from core.telegram import send_logs
from settings import LOG_FILE_PATH, CASE_DIR

logger = Logger(__name__).set_logger()


class App:

    @property
    def parser(self) -> OfficeSud:
        return OfficeSud(logger=logger)

    @staticmethod
    def get_data_to_upload() -> tuple[str, str]:
        iin = scan_folders()

        if iin is not None:
            statement_sum = get_statement_sum(CASE_DIR / iin)
            logger.info(f"Получили чек об оплате для ИИН: {iin}. Сумма иска: {statement_sum}")

            return iin, str(statement_sum)

    def run(self) -> None:
        try:
            iin, statement_sum = self.get_data_to_upload()
        except TypeError:
            logger.warning(f"Нет готовых исков для загрузки")
            return

        try:
            self.parser.process(iin, statement_sum)
        except Exception as process_error:
            logger.error(process_error, exc_info=True)
            send_logs(process_error.with_traceback(sys.exc_info()[2]), log_file=LOG_FILE_PATH)


trigger = IntervalTrigger(minutes=1)
scheduler = Scheduler(logger=logger)


if __name__ == '__main__':
    app = App()

    # try:
    scheduler.add_schedule(app.run, trigger)
    scheduler.start_in_background()
    # except (KeyboardInterrupt, SystemExit):
    #     logger.error('Interrupted')
    # except Exception as unexpected_error:
    #     logger.error(unexpected_error, exc_info=True)
    #     send_logs(unexpected_error, log_file=LOG_FILE_PATH)
