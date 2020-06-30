import logging

general_logger = logging.getLogger("general_logger")


def create_loggers(level=logging.DEBUG):
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    general_logger.addHandler(handler)
    general_logger.setLevel(level)
