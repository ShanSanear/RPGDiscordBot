import logging
import os
from logging.handlers import RotatingFileHandler

general_logger = logging.getLogger("general_logger")


def create_loggers(level=logging.DEBUG):
    """
    Creates loggers.
    :param level: Level by which to create logger.
    """
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s]:[%(name)-12s] [%(levelname).1s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = RotatingFileHandler(filename=os.getenv("LOG_FILE", "RPGDiscordBot.log"), mode='a',
                                       maxBytes=10240, backupCount=5, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    general_logger.addHandler(file_handler)
    stream_handler.setFormatter(formatter)
    general_logger.addHandler(stream_handler)
    general_logger.setLevel(level)
