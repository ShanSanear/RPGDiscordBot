import logging

general_logger = logging.getLogger("general_logger")


def create_loggers(level=logging.DEBUG):
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s]:[%(name)-12s] [%(levelname).1s]: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    general_logger.addHandler(handler)
    general_logger.setLevel(level)
