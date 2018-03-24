 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest
import time

from bot.tahmatassubot import CommandCache
from bot.command import Command

class TestCommandCache(unittest.TestCase):

  def test_instantiating_command_cache(self):
    command_cache = CommandCache(30)

  def test_init_max_cache_age(self):
    command_cache = CommandCache(30)
    self.assertEquals( command_cache.cache_max_age, 30)

  def test_len(self):
    command_cache = CommandCache(30)
    command_cache.set(Command("/listaa hae"), "")
    command_cache.set(Command("/listaa hae2"), "")
    command_cache.set(Command("/listaa hae3"), "")
    command_cache.set(Command("/listaa hae3"), "")
    self.assertEquals( len(command_cache), 3)

  def test_cache_cleaning(self):
    command1 = Command("/listaa hae")
    command2 = Command("/listaa hae2")

    command_cache = CommandCache(1)
    command_cache.set(command1, "")
    command_cache.set(command2, "")

    self.assertEquals(len(command_cache), 2)

    time.sleep(1.5)

    command_cache.is_command_cached( command1 )
    self.assertEquals(len(command_cache), 1)
    command_cache.is_command_cached( command2 )
    self.assertEquals(len(command_cache), 0)

if __name__ == '__main__':
  unittest.main()