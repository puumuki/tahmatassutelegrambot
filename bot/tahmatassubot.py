#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
import json
import signal
import sys
import logging
import requests
import time
import re

from bot.telegrambot import TelegramBot
from bot.telegrambot import ParseMode
from bot.command import Command
from bot.commandcache import CommandCache
from bot.cache import Cache
from bot import logger
from bot.logger import LOGGER_NAME

from bot.settings import TOKEN

class TahmaTassuBot(TelegramBot):

  def __init__(self, token, tahmatassu_base_url, bot_name="Tahmatassu Telegram bot"):
    """
    TahmaTassuBot class constructor
    
    Arguments:
      token {str} -- Telegram bot API token
      tahmatassu_base_url {str} -- Tahmatassu API url address
    
    Keyword Arguments:
      bot_name {str} -- Bot name (default: {"Tahmatassu Telegram bot"})
    """
    super(TahmaTassuBot, self).__init__(token=token, bot_name=bot_name)
    self.welcomeTmp = self.template('tahmatassuwelcome.md')
    self.ohjeTmp = self.template('tahmatassuohje.md')
    self._receipts_cache = Cache()
    self._search_cache = CommandCache()
    self._tahmatassu_base_url = tahmatassu_base_url
    self.logger = logging.getLogger(LOGGER_NAME) 

  def get_receipts(self):
    """Fetch receipts from Tahmatassu API.
    Receipts are fetched from Tahmatassu API by HTTP Get request and
    result is cached to memory.
    
    Returns:
      {list} -- Receipt objects are returned in a list
    """
    if self._receipts_cache.data == None or self._receipts_cache.is_cache_expried():
      self.logger.info("Fetching receipts")
      response = requests.get(self._tahmatassu_base_url+'/api/v2/recipes')
      
      if response.status_code == 200:
        self.logger.info("Tahmatassu server responded HTTP-status code 200, caching receipts.")
        self._receipts_cache.set( json.loads(response.text) )
      else:
        self.logger.info("Tahmatassu server responded HTTP-status code" + str(response.status_code))
    else:
      self.logger.info("Returning receipts from the cache")

    return self._receipts_cache.data
  
  def search_receipts( self, command ):
    """Search receipts from the Tahmatassu API
    
    Arguments:
      command {Command} -- Command containing search argument
    
    Returns:
      {list} -- Receipt object in a list
    """
    search_text = command.params[0]
    self.logger.info("Trying to /api/search/ "+search_text)
    response = requests.get(self._tahmatassu_base_url+'/api/search/' + search_text)
    
    if( response.status_code == 200 ):
      self.logger.info("Got result from server")
      search_result = json.loads(response.text)
      return list( map( lambda x: x[0].strip(), search_result ) )
    else:
      return []

  def get_receipt_title( self, receipt ):
    """Parses receipt title from the markdown string
    
    Arguments:
      receipt {dict} -- Receipt dict
    
    Returns:
      {str} -- Receipt title
    """
    lines = receipt.split('\n')
    return lines[0]

  def format_receipt_list_item( self, index, receipt ):
    """Return index and receipt title as string
    
    Arguments:
      index {int} -- index number
      receipt {str} -- receipt title
    
    Returns:
      {str} -- menu item
    """
    return str(index) + ' - ' + self.get_receipt_title( receipt.get('markdown') ) + '\n'

  def list_all_receips( self ):
    """Makes a list of available receipts
    
    Returns:
      {str} -- List of available receipts
    """
    titles = ''
    receipts = self.get_receipts()

    for index,receipt in enumerate(receipts):
      titles += str(index+1) + ' - ' + self.get_receipt_title( receipt.get('markdown') ) + '\n'

    return titles

  def list_searched_receipts( self, command ):
    """List searched receipts
    
    Arguments:
      command {Command} -- Search command
    
    Returns:
      {str} -- List of receipts
    """
    if self._search_cache.is_command_cached( command ):            
      titles = self._search_cache.get_cached_result( command )
      self.logger.info("Fetched cached search result: " + str(titles))
    else:
      titles = ''
      search_result = self.search_receipts( command )
      all_receipts = self.get_receipts()
      
      for index, receipt in enumerate(all_receipts):      
        if receipt.get('name') in search_result:
          titles += self.format_receipt_list_item( index + 1, receipt )
      
      self._search_cache.set(command, titles)
  
    return titles

  def list_receipts(self, command):
    """Search or list all receipts depending on the command.
    
    Arguments:
      command {Command} -- command object
    
    Returns:
      {str} -- List of receipts as string
    """
    if len(command.params) > 0:
      return self.list_searched_receipts( command )  
    else:    
      return self.list_all_receips()

  def get_receipt_number( self, text ):
    """Get receipt numbers
    
    Arguments:
      text {str} -- Get receipt number from command text
    
    Returns:
      {int} -- Return receipt number
    """
    try:
      params = text.split(' ')
      receipt_number = params[1] 
      return int(receipt_number)
    except (ValueError, IndexError) as e:
      return None

  def get_receipt(self, text):
    """Fetch a single receipt from the Tahmatassu API.
    
    Arguments:
      text {str} -- command text
    
    Returns:
      {str} -- Single receipt markdown text
    """
    receipt_number = self.get_receipt_number( text )
    receipts = self.get_receipts()
    
    if receipt_number and receipt_number > 0 and receipt_number <= len(receipts):  
      result =  self.cleanMarkdown( receipts[receipt_number - 1].get('markdown') )
      self.logger.info( result )
      return result
    else:
      return 'Hakemaasi reseptiä ei löytynyt'

  def handle_updates(self,updates):
    """Handle updates coming from the Telegram API
    
    Arguments:
      updates {dict} -- Update dictionary coming from Telegram API
    """
    for update in updates["result"]:
      try:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        
        if not Command.is_valid( text ):
          continue
          
        command = Command( text )

        if command.command in ['/list','/listaa', '/reseptit']:
          titles = self.list_receipts(command)
          self.send_message("Reseptit\n" + str(titles), chat)
        elif text in ['/help','/?','/ohje']:
          self.send_message(self.ohjeTmp, chat, parse_mode=ParseMode.MARKDOWN)
        elif "/get" in text or "/hae" in text:
          receipt = self.get_receipt(text)
          self.send_message(receipt, chat)
        elif text == "/start":
          self.send_message(self.welcomeTmp, chat, parse_mode=ParseMode.MARKDOWN)              
        else:
          self.send_message('meep', chat)
      except KeyError:
        continue

def main():
  """Main function for starting Tahmatassu bot
  """
  bot = TahmaTassuBot(TOKEN)
  bot.run()

#Signal handling
def signal_handler(signal, frame):
  """Signal handler takes process signal and handles them.
  
  Arguments:
    signal {???} -- ???
    frame {???} -- ???
  """
  logger = logging.getLogger('telegrambot')
  logger.info("CTRL+C pressed. Closing TahmatassuBot")
  sys.exit(0)

#Register signal handler
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
  main()