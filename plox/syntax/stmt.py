from abc import ABC, abstractmethod
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
    pass


class Var:
    def __init__(self, name: Token, initializer: Expr):
        """
        name is of type IDENTIFIER, which is the variable name.
        """
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Visitor):
        return visitor.visitVarStmt(self)


class If:
    pass


class Binary:
    pass
