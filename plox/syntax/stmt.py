from abc import ABC, abstractmethod
from plox.syntax import Visitor
from plox.syntax.expr import Expr


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
        """
        Syntax:
            exprStmt := expression ";" ;
        """
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        """
        Syntax:
            printStmt := "print" expression ";" ;
        """
        self.expression = expression
    
    def accept(self, visitor: Visitor):
        return visitor.visitPrintStmt(self)


class Block:
    pass


class Var:
    pass


class If:
    pass


class Binary:
    pass
