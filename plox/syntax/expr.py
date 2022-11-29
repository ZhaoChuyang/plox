from typing import List
from abc import ABC, abstractmethod
from plox.lexer.token import Token
from plox.syntax import Visitor


class Expr(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitAssignExpr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitBinaryExpr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitCallExpr(self)


class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object = object
        self.name = name
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitGetExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitLiteralExpr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitLogicalExpr(self)


class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitSetExpr(self)


class Super(Expr):
    def __init__(self, keyword: Token, method: Token):
        self.keyword = keyword
        self.method = method
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitSuperExpr(self)

class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitThisExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: Visitor) -> None:
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitVariableExpr(self)
    
    
