# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Tahmatassu Telegram bot runner script
"""
#pylint: disable=W0611
import bot.logger

from configparser import ConfigParser
from bot.tahmatassubot import TahmaTassuBot

def main():
  """Main function for starting for Tahmatassu Telegram bot.
  """
  config = ConfigParser()
  config.read("setting.ini")
  tahmatassu = TahmaTassuBot(
    token=config['DEFAULT']['token'],
    tahmatassu_base_url=config['DEFAULT']['tahmatassuapi'],
    bot_name=config['DEFAULT']['botname']
  )
  tahmatassu.run()

if __name__ == '__main__':
  main()