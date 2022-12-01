from plox.syntax.loxcallable import *
from plox.syntax import stmt
from plox.syntax.interpreter import *
from plox.syntax.enviroment import *
from plox.error import *
class loxfunction(loxcallable):

    declaration: stmt.Function
    closure: Environment

    def __init__(self, declaration: stmt.Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        environment = Environment(self.closure)
        for i in self.declaration.params.__sizeof__:
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return self.declaration.params.__sizeof__

    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"
