from abc import ABC, abstractmethod
from expr import *
from plox.lexer.token import *
from decimal import Decimal
from error import *
from enviroment import *
import string


class Interpreter(Visitor):###Visitor<Object>
    def __init__(self, environment: Environment):
        self.environment = environment




