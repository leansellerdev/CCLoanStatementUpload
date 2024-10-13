import logging
import colorlog

from settings import LOG_FILE_PATH


class Logger:
    def __init__(self, name: str, log_file: str = LOG_FILE_PATH, level: int = logging.INFO, to_file: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if to_file:
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            # Create formatter and add it to the file handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Create console handler with colorlog
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(filename)s:%(lineno)d - '
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(color_formatter)

        # Add the handlers to the logger
        self.logger.addHandler(console_handler)

    def set_logger(self):
        return self.logger

    def set_level(self, level: int):
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def add_file_handler(self, log_file: str, level: int = logging.INFO):
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def add_console_handler(self, level: int = logging.INFO):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(filename)s:%(lineno)d - '
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(color_formatter)
        self.logger.addHandler(console_handler)
