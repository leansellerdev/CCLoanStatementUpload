from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.browser.office_sud import OfficeSud
from core.scanning import get_statement_info, scan_folders

from loguru import logger

from settings import CASE_DIR


class App:

    @property
    def parser(self) -> OfficeSud:
        return OfficeSud(logger=logger)

    @staticmethod
    def get_data_to_upload() -> tuple[str, dict]:
        iin = scan_folders()

        if iin is not None:
            statement_info = get_statement_info(CASE_DIR / iin)

            return iin, statement_info

    def run(self) -> None:
        try:
            iin, statement_info = self.get_data_to_upload()
        except TypeError:
            logger.warning(f"Нет готовых исков для загрузки")
            return

        try:
            self.parser.process(statement_info)
        except Exception as process_error:
            logger.error(str(process_error), exc_info=True)


trigger = IntervalTrigger(minutes=1)
scheduler = BackgroundScheduler(logger=logger)


if __name__ == '__main__':
    app = App()

    try:
        scheduler.add_job(app.run, trigger)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Interrupted')
    except Exception as unexpected_error:
        logger.error(str(unexpected_error), exc_info=True)
        # send_logs(unexpected_error, log_file=LOG_FILE_PATH)
