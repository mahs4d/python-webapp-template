from abc import ABC
from functools import lru_cache

singleton = lru_cache


class Container(ABC):
    pass
