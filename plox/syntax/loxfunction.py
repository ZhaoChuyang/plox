from typing import List
from plox.syntax.loxcallable import LoxCallable
from plox.syntax import stmt
from plox.syntax.environment import Environment
from plox.syntax.ret import Return
from plox.syntax.loxinstance import LoxInstance


class LoxFunction(LoxCallable):

    def __init__(self, declaration: stmt.Function, closure: Environment, is_initializer: bool = False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance: LoxInstance) -> None:
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def call(self, interpreter, arguments: List[object]) -> object:
        # environment = Environment(self.closure)
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
