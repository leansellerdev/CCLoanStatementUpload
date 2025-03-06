from datetime import datetime, timedelta
import shutil

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.browser.office_sud import OfficeSud
from core import scanning

from loguru import logger

from core.telegram import send_logs
from settings import CASE_DIR, LOG_FILE_PATH


logger.add(LOG_FILE_PATH, encoding='utf-8')


class App:
    def __init__(self) -> None:
        self.parser = None

    @staticmethod
    def _init_parser() -> OfficeSud:
        parser = OfficeSud(logger=logger)
        return parser

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
        self.parser = self._init_parser()
        try:
            iin, statement_info = self.get_data_to_upload()
        except TypeError:
            logger.warning(f"Нет готовых исков для загрузки")
            return

        logger.info(f'ИИН: {iin}')

        if statement_info.get('final_summa') == 0:
            logger.info(f'Сумма иска равна {statement_info.get("final_summa")}. Удаляем дело!')
            shutil.rmtree(CASE_DIR / iin)
            return

        try:
            self.parser.process(statement_info)
        except Exception as process_error:
            self.parser.driver.quit()
            logger.error(str(process_error), exc_info=True)
            send_logs(message=str(process_error))


trigger = IntervalTrigger(minutes=1, start_date=datetime.now() + timedelta(seconds=5))
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
