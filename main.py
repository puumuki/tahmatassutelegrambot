# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Tahmatassu Telegram bot runner script
"""
#pylint: disable=W0611
import bot.logger

import logging
import argparse
import os

from configparser import ConfigParser
from bot.tahmatassubot import TahmaTassuBot
from bot.logger import LOGGER_NAME

def create_argparser():
  """Create command line argument parser.
  
  Returns:
    {argparse.ArgumentParser} -- Command line argument parser object
  """
  parser = argparse.ArgumentParser(description='Description of your program')
  parser.add_argument('-c', '--config', 
                      type=str, 
                      help='Config file, [setting.ini] file path', 
                      default="setting.ini", dest="config")
  parser.add_argument('-g', '--generate', 
                      type=str, 
                      help='Create initial configuration file, give file name and path as argument', 
                      dest="generate")
  parser.add_argument('-f', '--force', action='store_true', dest="force")
  return parser

def create_configuration_file(logger, args):
  """Generate initial configuration file
  
  Arguments:
    logger {Logger} -- logging object
    args {dict} -- Command line arguments
  """
  if not args.force and os.path.exists(args.generate):
    return logger.info("File exist allready, use -f flag to overwrite the existing file")
    
  config = ConfigParser()
  config.set('DEFAULT', 'token', 'Telegram Bot API token here')
  config.set('DEFAULT', 'tahmatassuapi', 'http://puumuki.game-server.cc')
  config.set('DEFAULT', 'botname', 'Tahmatassubot')
  
  with open(args.generate, 'w') as filehandle:
    config.write(filehandle)

  logger.info("Writed configuration to file named: " + args.generate)

def start_bot( logger, args ):
  """Create TahmatassuBot
  
  Arguments:
    logger {Logger} -- logger
    args {dict} -- Command line arguments
  """
  try:
    config = ConfigParser()
    config.read(args.config)
    tahmatassu = TahmaTassuBot(token=config['DEFAULT']['token'],
                               tahmatassu_base_url=config['DEFAULT']['tahmatassuapi'],
                               bot_name=config['DEFAULT']['botname'])
    tahmatassu.run()
  except Exception as error:
    logger.error(error)
    logger.exception("message")

def main():
  """Main function for starting for Tahmatassu Telegram bot.
  """
  log = logging.getLogger(LOGGER_NAME)

  parser = create_argparser()
  args = parser.parse_args()

  if args.generate:
    create_configuration_file(log, args)
  else:
    start_bot(log, args)



if __name__ == '__main__':
  main()