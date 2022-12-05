from plox.lexer.token import Token
from plox.error import PLoxRuntimeError


class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = dict()

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_function(name.lexeme)
        if method is not None: 
            return method.bind(self)
        
        raise PLoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name: Token, value: object) -> None:
        self.fields[name.lexeme] = value

    def __repr__(self):
        return f"{self.klass} instance"