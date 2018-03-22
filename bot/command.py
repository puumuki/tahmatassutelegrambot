import re
import time

class Command():

  COMMAND_REGEXP = r"^\/([a-z0-9_])+(\@[a-z]\w*(_\w+)*)?([ \f\n\r\t\v\u00A0\u2028\u2029].*)?$"

  def __init__(self, text, chat=None):
    self.parse_command( text )
    self.created = time.time()
    self.chat = chat
    
  def parse_command(self, text ):
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
    exp = re.compile( Command.COMMAND_REGEXP )
    return exp.match( text ) != None