from typing import List
from plox.syntax.loxcallable import LoxCallable
from plox.syntax import stmt
from plox.syntax.environment import *
from plox.syntax.ret import Return


class LoxFunction(LoxCallable):

    def __init__(self, declaration: stmt.Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments: List[object]) -> object:
        # environment = Environment(self.closure)
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
