# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Tahmatassu Telegram bot runner script
"""
#pylint: disable=W0611
import bot.logger

import logging

from configparser import ConfigParser
from bot.tahmatassubot import TahmaTassuBot
from bot.logger import LOGGER_NAME

def main():
  """Main function for starting for Tahmatassu Telegram bot.
  """
  log = logging.getLogger(LOGGER_NAME)

  try :
    config = ConfigParser()
    config.read("setting.ini")
    tahmatassu = TahmaTassuBot(
      token=config['DEFAULT']['token'],
      tahmatassu_base_url=config['DEFAULT']['tahmatassuapi'],
      bot_name=config['DEFAULT']['botname']
    )
    tahmatassu.run()
  except Exception as error:
    log.error( error )
    log.exception("message")

if __name__ == '__main__':
  main()