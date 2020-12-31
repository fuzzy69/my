import logging
from logging import (
    Logger,
    getLogger,
    FileHandler,
    Formatter,
    StreamHandler,
    DEBUG,
    INFO,
)
from typing import AnyStr, Optional, Union

try:
    from libs.my.core.meta.dummy_object import DummyObject
except ModuleNotFoundError:
    from core.meta.dummy_object import DummyObject


LOG_FORMAT = (
    "%(asctime)s [%(name)s] <%(threadName)s> %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S",
)


def create_logger(
    name: AnyStr,
    level: logging.INFO = INFO,
    log_format: AnyStr = LOG_FORMAT,
    log_to_console: bool = True,
    log_file: Optional[AnyStr] = None,
) -> Union[Logger, DummyObject]:
    """
    Creates console and/or file logging instance
    :param str name: logger instance name, usually current python file
    :param int level: logging level, recommended DEBUG for development and INFO for production
    :param tuple log_format: tuple of outputs log message format and log time
    :param str log_file: path to log file
    :return: logging.Logger instance
    """
    if any((log_to_console, log_file)):
        logging.propagate = False
        logger = getLogger(name)
        logger.setLevel(level)
        formatter = Formatter(*log_format)
        # Remove all existing handlers
        logger.handlers = []
        # Console handler
        if log_to_console:
            ch = StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        # File handler
        if log_file is not None:
            fh = FileHandler(log_file)
            fh.setLevel(DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    else:
        logger = DummyObject()

    return logger
