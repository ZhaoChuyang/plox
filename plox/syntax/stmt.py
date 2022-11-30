from abc import ABC, abstractmethod
from typing import List
from plox.syntax import Visitor
from plox.syntax.expr import Expr
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
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch :Stmt):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitIfStmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitWhileStmt(self)