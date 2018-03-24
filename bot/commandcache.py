"""CommandCache is way to store command results and reuse them later.
"""
import time
import logging

class CommandCache():
  """CommandCache is way to store command results and reuse them later.
  """

  def __init__(self, cache_max_age=60*5):
    """Constructor
    
    Keyword Arguments:
      cache_max_age {int} -- Cached command max age in seconds (default: {60*5})
    """
    self.commands = {}
    self.cache_max_age = cache_max_age
    self.logger = logging.getLogger('telegrambot')

  def is_command_cached(self, command):
    """Thes is command cached and fresh enough to be used.. :)
    
    Arguments:
      command {Command} -- Command object
    
    Returns:
      {boolean} -- Return true if command is cached false if not
    """
    cached_command = self.commands.get(command, False)    
    
    if cached_command != False:      
      return self.commands[command].created + self.cache_max_age < time.time()
      #TODO: Clean cached command after command is aged..
    else:
      return False
  
  def get(self, command):
    """Return cached command object from the cache
    
    Arguments:
      command {[type]} -- [description]
    
    Returns:
     {Command} -- Return Command instance if found, otherwise return None
    """
    self.logger.debug("Fetching cached command: " + command.command)
    return self.commands.get(command, None)
  
  def get_cached_result(self, command):
    """Return command object cached result
    
    Arguments:
      command {Command} -- Command object as param
    
    Returns:
      {*} -- Return command's cached result. Can be string or object or list you decide..
    """
    cached_command = self.get(command)
    return cached_command and cached_command.result if command else None

  def set(self, command, result):
    """Caches command object and it's result to the command cache.
    
    Arguments:
      command {Command} -- Command object
      result {*} -- Command object result. Can be string or object or list you decide..
    """
    self.logger.debug("Caching command: " + command.command + str(command.params))
    command.result = result 
    self.commands[command] = command
