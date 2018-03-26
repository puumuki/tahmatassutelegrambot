# -*- coding: utf-8 -*-
"""Hold logic form creating a Telegram bot. 
By using TelegramBot as base class for your both you get premade 
functionality to impelemnt your bot.

This both is based to this tutorial:
https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
"""
import json
import requests
import time
import urllib
import logging
import os
import re

from bot.logger import LOGGER_NAME
from bot.logger import MESSAGE_LOGGER

from bot.settings import LONG_POLL_TIMEOUT
from bot.settings import TOKEN
from bot.settings import TELEGRAM_SERVER_URL
from bot.settings import TEMPLATE_DIR

class ParseMode:
  """This is how Telegram API handles message that your
  bot send to the Telegram API. There is support for plaintext,
  markdown and HTML. Use this with the TelegramBot::send_message method.
  """
  MARKDOWN = 'Markdown'
  HTML = 'HTML'
  PLAINTEXT = None

class TelegramBotException(Exception):
  def __init__(self, message):
    super(TelegramBotException, self).__init__(message)

class TelegramBot(object):
  """TelegramBot class is base class for implementing a
  telegram bot. By using this class as base class of the
  telegram bot implementation you get all basic funtionalities
  to do your own Telegram bot. 
  
  Raises:
    TelegramBotException -- Generig TelegramBot exception class
  """

  def __init__(self, token, bot_name="Tahmatassubot"):
    """TelegramBot constructor

    Keyword Arguments:
      token {str} -- Telegram bot unique identication id
      bot_name {str} -- Bot name, just a name..] (default: {"Tahmatassubot"}
    
    Raises:
      TelegramBotException -- Raised on Telegram API token is missing 
    """
    if type(token) is not str or len(token) == 0:
      raise TelegramBotException("Telegram API token missing") 

    if type(bot_name) is not str or len(bot_name) == 0:
      raise TelegramBotException("Telegram bot has no name, give a name or use default name")

    self.bot_name = bot_name
    self.token = token
    self.url = TELEGRAM_SERVER_URL.format(token)
    self._chats = {}
    self.msg_logger = logging.getLogger(MESSAGE_LOGGER)
    self.logger = logging.getLogger(LOGGER_NAME)
    self.logger.info( self.url )

  def get_url(self, url):
    """Makes a HTTP Get request to Telegram API
    
    If an ConnectionError occurs connection is tried after 4 seconds again.

    Returns:
      str -- Return HTTP request content (JSON data)
    """
    try:      
      self.msg_logger.info( url )

      response_content = None
      response = requests.get(url)
      
      self.msg_logger.debug("RESPONSE:")
      self.msg_logger.debug( response.status_code )

      if response.status_code == 200:      
        response_content = response.content.decode("utf8")
      else:
        self.msg_logger.error("RESPONSE:")
        self.msg_logger.error( response.status_code )
        self.msg_logger.error( response.content.decode("utf8") )

      self.msg_logger.debug( response_content )

      return response_content

    except requests.exceptions.ConnectionError as error:
      self.logger.error("Connection error: " + str(error))
      self.logger.info("Retrying request after couple seconds")
      time.sleep(4)
      return self.get_url(url)

  def get_json_from_url(self, url):
    """Makes a HTTP Get request to Telegram API. 
    The response is parser to JSON object witch then is retunerd
    as return value.
    
    Arguments:
      url {string} -- [Query string]
    
    Returns:
      dict -- [Return deserialized JSON object]
    """
    content = self.get_url(url)
    js = json.loads(content)
    return js

  def get_updates(self, offset=None):
    """Makes HTTP request as a long poll to Telegram API
    
    Keyword Arguments:
      offset {int} -- Message queue offset (default: {None})
    
    Returns:
      dict -- Return deserialised JSON object
    """
    url = self.url + "getUpdates?timeout=" + LONG_POLL_TIMEOUT
    if offset:
      url += "&offset={}".format(offset)
    js = self.get_json_from_url(url)
    return js

  def get_last_update_id(self, updates):
    """Get maximum update ID number from the updates
    
    Arguments:
      updates {list} -- Update objects from Telegram API
    
    Returns:
      {int} -- Integer update number
    """
    update_ids = []
    for update in updates["result"]:
      update_ids.append(int(update["update_id"]))
    return max(update_ids)

  def send_message(self, text, chat_id, reply_markup=None, parse_mode=None):
    """Send a message to TelegramAPI
    
    Arguments:
      text {str} -- Message to send to the chat
      chat_id {int} -- chat identification number, comes with update messages
    
    Keyword Arguments:
      reply_markup {object} -- Custom keyboards and much more.. 
      parse_mode {ParseMode} -- Can be markdown or HTML, if None is passed planetext is used
    """
    text = urllib.parse.quote_plus(text)
    url = self.url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
      url += "&reply_markup={}".format(reply_markup)
    if parse_mode:
      url += "&parse_mode={}".format(parse_mode)
    self.get_url(url)

  def template( self, name ):
    """Load template file from the template directory.
    
    TelegramAPI supports simple form of Markdown ;)
    
    Arguments:
      name {string} -- Template file name
    
    Raises:
      TelegramBotException -- Exception is raised if template is not found
    
    Returns:
      string -- Template file content
    """
    path = os.path.join( TEMPLATE_DIR, name )    
    
    if os.path.exists( path ):
      with open(path,'r') as handle:
        return handle.read()
    else:
      raise TelegramBotException("Template %s not found" % (name,))

  def handle_updates(self, updates):
    """This is where messages from Telegram API ends up.
    Each update is handled here one by one. 
    
    This method you want to overwrite on extending class.
    
    Arguments:
      updates {array} -- Updates as update object, read more from TelegramAPI
    """
    for update in updates["result"]:
      try:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]

        last_time_sended = self._chats.get(chat, 1)

        #Make sure that we don't spam Telegram API.. this way every one using bot waits..
        #TODO: Find better way to do this..
        if ( last_time_sended - time.time() ) < 1:
          time.sleep( 1 )

        #Keep track when message was sended to particular chat.  
        self._chats[chat] = time.time()        
        self.send_message(text, chat)        
      except Exception as e:
        self.logger.error(e)

  def clean_markdown(self, markdown):
    """Clean markdown going to Telegram API
    
    Arguments:
      markdown {str} -- markdown string
    
    Returns:
      {str} -- cleaned markdown string
    """
    #Clean up links from the markdown, these don't go trough Telegram Bot API
    regex = r"!\[(.*?)\]\(.*?\)" 
    result = re.sub(regex, '', markdown)

    #Replace single '*' letters with '-' marker
    #Telegram API is expecting to have bolded text with two '*' marker surraunding
    #the bolded text and gives and error if there is uneven amount of '*' markers around.
    last_result = ''

    for line in result.split('\n'):

      if line.count('*') == 1: 
        last_result += line.replace('*','-') + '\n'
      else:
        last_result += line + '\n'

    return last_result.strip()

  def run(self):
    """Calling this function start the actual TelegramBot.
    After instanciating TelegramBot object you need to call 
    this to start the bot and start listening updates from 
    the Telegram API.
    """
    self.logger.info("Starting the " + self.bot_name)

    last_update_id = None

    while True:
      updates = self.get_updates(last_update_id)
      if len(updates.get("result",[])) > 0:
        last_update_id = self.get_last_update_id(updates) + 1
        self.handle_updates(updates)
      time.sleep(0.5)
