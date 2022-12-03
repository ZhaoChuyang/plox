from plox.error import PLoxRuntimeError
from plox.lexer.token import Token


class Environment:
    def __init__(self, enclosing = None):
        """
        Args:
            enclosing (Enviroment): the immediately closing Enviroment outside of current Enviroment.
        """
        self.enclosing = enclosing
        self.values = {}
    
    def define(self, name: str, value: object) -> None:
        """
        binds the value to a specified variable name.
        """
        self.values[name] = value
    
    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values.get(name)
    
    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment =  environment.enclosing
        return environment

    def get(self, name: str) -> object:
        if name in self.values:
            return self.values[name]
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise PLoxRuntimeError(name, f"Variable {name} does not exist.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise PLoxRuntimeError(name, f"Undefined variable {name.lexeme}.")
