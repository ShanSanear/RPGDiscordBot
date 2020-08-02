import logging
import sys

general_logger = logging.getLogger("general_logger")


def custom_exception_logging(exctype, value, traceback):
    general_logger.exception('Exception type: %s', exctype)
    general_logger.exception('Exception Value: %s', value)
    general_logger.exception('Exception traceback: %s', traceback)


sys.excepthook = custom_exception_logging


def create_loggers(level=logging.DEBUG):
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s]:[%(name)-12s] [%(levelname).1s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(filename='RPGDiscordBot.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    general_logger.addHandler(file_handler)
    stream_handler.setFormatter(formatter)
    general_logger.addHandler(stream_handler)
    general_logger.setLevel(level)
