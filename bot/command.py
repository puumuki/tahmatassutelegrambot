"""Module hold Command class logic.
"""

import re
import time

class Command():
  """Command class hold single Telegram message witch is parsed by this 
  class to a command. All messages with start with '/' sign are considered commands.

  A command has always name and parameters. If the command string is '/list meat' then
  the /list is the command and meat is the parameter. There can be 0 to n parameters.
  """
  
  """Regular expression to validate command string
  """
  COMMAND_REGEXP = r"^\/([a-z0-9_])+(\@[a-z]\w*(_\w+)*)?([ \f\n\r\t\v\u00A0\u2028\u2029].*)?$"

  def __init__(self, text, chat=None):
    """Constructor
    
    Arguments:
      text {str} -- Command string to be parsed
    
    Keyword Arguments:
      chat {int} -- Chat identification number (default: {None})
    """
    self.parse_command( text )
    self.created = time.time()
    self.chat = chat
    
  def parse_command(self, text ):
    """Parses text to command objet    
    
    Arguments:
      text {str} -- Command string
    """
    self._text = text
    parts = text.split(' ')
    if len(parts) > 1:
      self.command = parts[0]
      self.params = parts[1:]
    elif len(parts) == 1:
      self.command = parts[0]
      self.params = []

  def __hash__(self):
    return hash(self._text)

  def __eq__(self, other):    
    return isinstance(other, self.__class__) and self._text == other._text
 
  def __str__(self):
    return "Command: " + self.command + " - Params: " + str(self.params)

  @staticmethod
  def is_valid( text ):
    """Test is text a valid command
    
    Arguments:
      text {str} -- Command text
    
    Returns:
      {boolean} -- Return true is text is valid command false if not
    """

    exp = re.compile( Command.COMMAND_REGEXP )
    return exp.match( text ) != None