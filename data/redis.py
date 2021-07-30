import os
from walrus import *

_REDIS_URL = os.getenv('REDIS_URL')
_db = Database.from_url(_REDIS_URL)
polls = _db.Hash("polls")