"""Hold Tahmamatassu Telegram bot's logging settings
"""
import logging

LOGGER_NAME = 'telegrambot'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('telegrambot.log')
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
