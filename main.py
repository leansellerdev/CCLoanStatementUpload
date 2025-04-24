import os
from datetime import datetime, timedelta
import shutil

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from selenium.common import TimeoutException

from core.browser.office_sud import OfficeSud
from core import scanning

import traceback
from loguru import logger

from core.scanning import get_total_todays_cases
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
        folder_name = scanning.scan_folders()

        if folder_name is not None:
            try:
                statement_info = scanning.get_statement_info(CASE_DIR / folder_name)
            except FileNotFoundError as no_statement_info:
                logger.error(str(no_statement_info), exc_info=True)
                send_logs(message=f'Нет информации об иске для ИИН: {folder_name}')
            else:
                return folder_name, statement_info

    def run(self) -> None:
        try:
            folder_name, statement_info = self.get_data_to_upload()
        except TypeError:
            logger.warning(f"Нет готовых исков для загрузки")
            return
        else:
            self.parser = self._init_parser()

        logger.info(f'ИИН: {folder_name}')

        if statement_info.get('final_summa') == 0:
            logger.info(f'Сумма иска равна {statement_info.get("final_summa")}. Удаляем дело!')
            shutil.rmtree(CASE_DIR / folder_name)
            return

        try:
            self.parser.process(statement_info)
        except TimeoutException:
            self.parser.driver.quit()
        except Exception:
            self.parser.driver.quit()
            send_logs(message=traceback.format_exc())
            logger.error(traceback.format_exc())

    def start(self) -> None:
        today_cases = get_total_todays_cases()
        logger.info(f'Количество дел за сегодня: {today_cases}')

        if today_cases >= 40:
            return

        self.run()


trigger = IntervalTrigger(minutes=1, start_date=datetime.now() + timedelta(seconds=5))
scheduler = BlockingScheduler()


if __name__ == '__main__':
    app = App()

    try:
        scheduler.add_job(app.start, trigger)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Interrupted')
    except Exception as unexpected_error:
        send_logs(message=traceback.format_exc())
        logger.error(unexpected_error)
