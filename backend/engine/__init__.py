#!/usr/bin/python3

from engine.db_storage import Storage
from engine.cache_storage import LRUCache

storage = Storage()
lrucache = LRUCache()
storage.cache = lrucache
storage.reload()
