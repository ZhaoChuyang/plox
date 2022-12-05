from abc import ABC, abstractmethod
from typing import List
from plox.syntax import Visitor
from plox.syntax.expr import Expr, Variable
from plox.lexer.token import Token


class Stmt(ABC):
    """
    Base class for all statements.
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor: Visitor):
        return visitor.visitPrintStmt(self)



class Block:
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor: Visitor):
        return visitor.visitBlockStmt(self)


class Var:
    def __init__(self, name: Token, initializer: Expr):
        """
        name is of type IDENTIFIER, which is the variable name.
        """
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Visitor):
        return visitor.visitVarStmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch :Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitIfStmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitWhileStmt(self)
"""
  new in 10
"""
class Function(Stmt):
    def __init__(self,name: Token, params: List[Token], body: List[Stmt]):
        self.name = name
        self.params = params
        self.body = body
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitFunctionStmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitReturnStmt(self)


class Class(Stmt):
    def __init__(self, name: Token, superclass: Variable, methods: List[Function]):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitClassStmt(self)
