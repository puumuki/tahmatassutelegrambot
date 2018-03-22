import time
import logging

from bot import logger

class CommandCache():

  def __init__(self,cache_max_age = 60):
    self.commands = {}
    self.cache_max_age = cache_max_age
    self.logger = logging.getLogger('telegrambot')

  def is_command_cached(self, command):
    cached_command = self.commands.get(command, False)    
    
    if cached_command != False:      
      return self.commands[command].created + self.cache_max_age < time.time()
    else:
      return False
  
  def get(self, command):
    self.logger.debug("Fetching cached command: " + command.command)
    return self.commands[command]
  
  def get_cached_result(self, command):
    cached_command = self.get(command)
    return cached_command.result if command else None

  def set(self, command, result):
    self.logger.debug("Caching command: " + command.command + str(command.params))
    command.result = result 
    self.commands[command] = command