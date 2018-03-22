 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import unittest
from bot.command import Command

class TestCommand(unittest.TestCase):

  def test_equality(self):
    command = Command("/listaa haku")
    command2 = Command("/listaa haku")
    self.assertEqual( command, command2)

  def test_inequality(self):
    command = Command("/listaa haku")
    command2 = Command("/listaa haku2")
    self.assertNotEqual(command, command2)    

  def test_parsing_with_two_params(self):
    command = Command("/listaa liha kauppa")
    self.assertEqual( len(command.params), 2 )
    self.assertEqual( command.params[0], "liha" )
    self.assertEqual( command.params[1], "kauppa" )
    self.assertTrue( isinstance(command.params, list) )
    self.assertTrue( isinstance(command.command, str) )

  def test_parsing_with_zero_params(self):
    command = Command("/listaa")
    self.assertEqual( len(command.params), 0 )
    self.assertTrue( isinstance(command.params, list) )
    self.assertTrue( isinstance(command.command, str) )

  def test_not_command(self):
    command = Command("listaa")
    self.assertEqual( len(command.params), 0 )
    self.assertTrue( isinstance(command.params, list) )
    self.assertTrue( isinstance(command.command, str) ) 

  def test_is_valid_command(self):
    self.assertTrue( Command.is_valid( "/listaa" ) )
    self.assertTrue( Command.is_valid( "/listaa haku" ) )
    self.assertTrue( Command.is_valid( "/listaa haku paku" ) )
    self.assertTrue( Command.is_valid( "/listaa 2" ) )
    self.assertFalse( Command.is_valid( "listaa 2" ) )
    self.assertFalse( Command.is_valid( "/" ) )

  def test_str(self):
    self.assertEqual(str(Command('/listaa liha')), "Command: /listaa - Params: ['liha']" )
    
if __name__ == '__main__':
  unittest.main()