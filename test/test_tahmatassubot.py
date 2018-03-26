 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import unittest

from bot.tahmatassubot import TahmaTassuBot
from bot.telegrambot import TelegramBotException

test_receipt =  """Pinaattiletut
=========
 * 2 munaa
 * 0,5l maitoa
 * 3dl jauhoa
 * tuoretta muserrettua pinaattia
 * ripaus suolaa

 * Boldattu *

Silppua pinaatti tehosekoittimella pieneksi. Riko kananmunat kulhoon. Sekoita maito, suola, vehnäjauhot ja silputtu pinaatti joukkoon. Voit lisätä myös lorauksen öljyä joukkoon. Voit antaa taikinan turvota puolisen tuntia. Paista kuumalla pannulla.

![Pinaattilettutaikina](http://puumuki.game-server.cc/static/img/pinaattilettutaikina.jpg)
![Pinaattilettu paistuvat pannulla](http://puumuki.game-server.cc/static/img/pinaattiletut-pannulla.jpg)
"""

test_receipt_result = """Pinaattiletut
=========
 - 2 munaa
 - 0,5l maitoa
 - 3dl jauhoa
 - tuoretta muserrettua pinaattia
 - ripaus suolaa

 * Boldattu *

Silppua pinaatti tehosekoittimella pieneksi. Riko kananmunat kulhoon. Sekoita maito, suola, vehnäjauhot ja silputtu pinaatti joukkoon. Voit lisätä myös lorauksen öljyä joukkoon. Voit antaa taikinan turvota puolisen tuntia. Paista kuumalla pannulla."""


class TestTelegramBot(unittest.TestCase):

  def test_instantiating_wihtout_token(self):    
    with self.assertRaises(TelegramBotException) as context:
      TahmaTassuBot('', bot_name='Tahmatassu', tahmatassu_base_url='')
      self.assertTrue('Telegram API token missing' in context.exception)

  def test_instantiating_wihtout_bot_name(self):    
    with self.assertRaises(TelegramBotException) as context:
      TahmaTassuBot('sdafasd', bot_name='', tahmatassu_base_url='')
      self.assertTrue("Telegram bot has no name, give a name or use default name" in context.exception)      

  def test_cleaning_receipt(self):
    bot = TahmaTassuBot('Test', bot_name='Test Bot', tahmatassu_base_url='')
    result = bot.clean_markdown(test_receipt)
    self.assertEquals(result, test_receipt_result)

if __name__ == '__main__':
  unittest.main()


