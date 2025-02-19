from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.browser.office_sud import OfficeSud
from core import scanning

from loguru import logger

from core.telegram import send_logs
from settings import CASE_DIR, LOG_FILE_PATH


logger.add(LOG_FILE_PATH)


class App:

    @property
    def parser(self) -> OfficeSud:
        return OfficeSud(logger=logger)

    @staticmethod
    def get_data_to_upload() -> tuple[str, dict]:
        iin = scanning.scan_folders()

        if iin is not None:
            try:
                statement_info = scanning.get_statement_info(CASE_DIR / iin)
            except FileNotFoundError as no_statement_info:
                logger.error(str(no_statement_info), exc_info=True)
                send_logs(message=f'Нет информации об иске для ИИН: {iin}')
            else:
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
            logger.error(str(process_error), exc_info=True
            )
            send_logs(message=str(process_error))


trigger = IntervalTrigger(minutes=1)
scheduler = BlockingScheduler(logger=logger)


if __name__ == '__main__':
    app = App()

    try:
        scheduler.add_job(app.run, trigger)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Interrupted')
    except Exception as unexpected_error:
        logger.error(str(unexpected_error), exc_info=True)
        send_logs(message=str(unexpected_error))
