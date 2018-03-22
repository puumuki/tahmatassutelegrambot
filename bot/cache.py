import time

class Cache():

  def __init__(self, data=None, cache_max_age = 60):
    self.cache_max_age = cache_max_age
    self.set( data )

  def is_cache_expried(self):
    return self.cache_time + self.cache_max_age < time.time()

  def set(self, data):
    self.cache_time = time.time()
    self.data = data