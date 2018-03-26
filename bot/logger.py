"""Hold Tahmamatassu Telegram bot's logging settings
"""
import logging
from logging.handlers import RotatingFileHandler

LOGGER_NAME = 'telegrambot.log'

MESSAGE_LOGGER = 'messagelogger.log'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
FILE_SIZE = 1000 * 10 ** 3  
BACK_UP_COUNT = 10

fh = RotatingFileHandler(LOGGER_NAME, 'a', FILE_SIZE, BACK_UP_COUNT)
fh.setLevel(logging.INFO)

# logger for debugging Telegram message traffic
msg_logger = logging.getLogger(MESSAGE_LOGGER)
msg_logger.setLevel(logging.DEBUG)

ms = RotatingFileHandler(MESSAGE_LOGGER, 'a', FILE_SIZE, BACK_UP_COUNT)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
ms.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# add the handlers to msg_logger
msg_logger.addHandler(ms)
