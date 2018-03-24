 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import unittest

from bot.tahmatassubot import Cache

class TestCache(unittest.TestCase):

  def test_cache(self):
    cache = Cache({}, 30)
    self.assertEquals(cache.cache_max_age, 30)    

  def test_expiring_cache(self):
    cache = Cache({}, 30)
    self.assertFalse(cache.is_cache_expried())
    cache.cache_max_age = 0
    self.assertTrue(cache.is_cache_expried())

if __name__ == '__main__':
  unittest.main()