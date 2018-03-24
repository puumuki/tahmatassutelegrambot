"""Cache module holds Cache class logic.
"""
import time

class Cache():
  """Cache is a generic cache object for any type of data.
  Cache invalidation is based on just time. TahmatassuTelegramBot uses 
  cache as a way storing recipe objects fetched from the Tahmatassu server so 
  it don't need to fetch recipes every single request again and again.
  """

  def __init__(self, data, cache_max_age = 60*5):
    """Constructor
    
    Keyword Arguments:
      data {*} -- Cached data, object or dictionary or list.. what ever.
      cache_max_age {int} -- Time in seconds how long cache is hold (default: {60*5} five minutes)
    """
    self.cache_max_age = cache_max_age
    self.set( data )

  def is_cache_expried(self):
    """Return is cache expired
    
    Returns:
      boolean -- Return true if cache is expired
    """
    return self.cache_time + self.cache_max_age < time.time()

  def set(self, data):
    """Set cache content and reset cache internal counter
    
    Arguments:
      data {*} -- Cached data, object or dictionary or list.. what ever.
    """
    self.cache_time = time.time()
    self.data = data