 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import unittest

from bot.tahmatassubot import TelegramBot
from bot.telegrambot import TelegramBotException

class TestTelegramBot(unittest.TestCase):

  def test_instantiating_wihtout_token(self):    
    with self.assertRaises(TelegramBotException) as context:
      TelegramBot('', bot_name='Tahmatassu')
      self.assertTrue('Telegram API token missing' in context.exception)

  def test_instantiating_wihtout_bot_name(self):    
    with self.assertRaises(TelegramBotException) as context:
      TelegramBot('sdafasd', bot_name='')
      self.assertTrue("Telegram bot has no name, give a name or use default name" in context.exception)      

if __name__ == '__main__':
  unittest.main()