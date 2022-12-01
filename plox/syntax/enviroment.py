from plox.error import PLoxRuntimeError
import string
from plox.lexer.token import *
class Environment:
    def __init__(self):
        self.values = {}
    
    def define(self, name: str, value: object) -> None:
        """
        binds the value to a specified variable name.
        """
        self.values[name] = value
    
    def get_at(self, distance: int, name: string) -> object:
        return self.ancestor(distance).values.get(name)
    
    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance: int) -> 'Environment':
        environment = self
        for i in range(0,distance):
            environment =  environment.enclosing
        return environment


    def get(self, name: str) -> object:
        if name in self.values:
            return self.values[name]
        
        raise PLoxRuntimeError(name, f"Variable {name} does not exist.")