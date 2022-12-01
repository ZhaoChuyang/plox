from typing import List
from abc import ABC, abstractmethod
from time import time


class LoxCallable(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments: List[object]) -> object:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass

"""
Built-in Callables
"""

class Clock(LoxCallable):
    def call(self, interpreter, arguments: List[object]):
        return time()
    
    def arity(self):
        return 0

    def __str__(self):
        return "<native fn>"