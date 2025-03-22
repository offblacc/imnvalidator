# config.py

from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent # assuming structure: PROJECT_ROOT/py/validate.py

def configure_logging(log_to_file=True, log_file="imnvalidator.log"):
    logger = logging.getLogger("imnvalidator")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    if logger.hasHandlers():
        logger.handlers.clear()

    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    else:
        syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
        syslog_handler.setLevel(logging.DEBUG)
        logger.addHandler(syslog_handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    for handler in logger.handlers:
        handler.setFormatter(formatter)

    return logger

class Config:
    def __init__(self):
        self.VERBOSE = False
        self.logger = configure_logging()
        self.imunes_filename = None
        self.test_config_filename = None

    def set_verbose(self, verbose):
        self.VERBOSE = verbose

class State:
    def __init__(self):
        self.imunes_output = ''
        self.eid = None

config = Config()
state = State()
