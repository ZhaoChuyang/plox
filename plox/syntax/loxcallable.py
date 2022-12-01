from plox.syntax.interpreter import Interpreter
from abc import ABC, abstractmethod
from time import time

class loxcallable(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        pass
    @abstractmethod
    def arity(self) -> int:
        pass

class loxcallable_2(loxcallable):
    def arity(self):
        return 0
    def call(self, interpreter: Interpreter, arguments: list):
        return float(time())
    def __str__(self):
        return "<native fn>"