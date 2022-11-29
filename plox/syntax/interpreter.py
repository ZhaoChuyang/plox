from abc import ABC, abstractmethod
from expr import *
from plox.lexer.token import *
from decimal import Decimal
from error import *
from enviroment import *
import string
class Interpreter(Visitor):###Visitor<Object>
    def __init__(self, environment: Environment):
        self.environment = environment


    def _interpret(self, statements) -> None:
        try: 
            for statement in statements:
                self._execute(statement)
        except RuntimeError as e:
            runtimeError(e)

    def _execute(self, stmt: Stmt):
        stmt.accept(self)

    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statement, Environment(self.environment))
        return None
    
    def executeBlock(self, statements, environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous

    def _stringify(self, object: object) -> string:
        if object is None :return "nil"
        if isinstance(object, float):
            text = string(object)
            if text.endswith(".0"):
                text = text[0, text.length-2]
            return text
        return string(object)

    def visitLiteralExpr(self, expr: Literal) -> object:
        return expr.value
    
    """
    new 
    new in ch9
    """
    def visitLogicalExpr(self, expr: Logical):
        left = self._evaluate(expr.left)
        if isinstance(expr.operator.type, OR):
            if self._isTruthy(left):
                return left
        else:
            if not self._isTruthy(left):
                return left
        return self._evaluate(expr.right)

    def _isTruthy(self, object: object) -> bool:
        if object is None:
            return False
        if isinstance(object,bool):
            return bool(object)
        return True

    def visitUnaryExpr(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)
        
        if isinstance(expr.operator.type, MINUS):
            self._checkNumberOperand(expr.operator, right)
            return -float(right)
        elif isinstance(expr.operator.type, BANG):
            return self._isTruthy(right)

        return None

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)


    
    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
    
    """
    new in 8.1.3
    """
    def visitExpressionStmt(self, stmt: Expression):
        self._evaluate(stmt.expression)
        return None
    
    
    def visitPrintStmt(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value)+"\n")
        return None
    
    def visitVarStmt(self,stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitAssignExpr(self, expr: Assign) -> object:
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    """
    new in ch9
    """
    def visitIfStmt(self, stmt: If):
        if self._isTruthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self._execute(stmt.elseBranch)
        return None

    def visitBinaryExpr(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        if isinstance(expr.operator.type, GREATER):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        elif isinstance(expr.operator.type, GREATER_EQUAL):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        elif isinstance(expr.operator.type, LESS):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        elif isinstance(expr.operator.type, LESS_EQUAL):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)
        elif isinstance(expr.operator.type, MINUS):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif isinstance(expr.operator.type, PLUS):
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, string) and isinstance(right, string):
                return string(left) + string(right)
        elif isinstance(expr.operator.type, SLASH):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        elif isinstance(expr.operator.type, STAR):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        elif isinstance(expr.operator.type, BANG_EQUAL):
            return not self._isEqual(left,right)
        elif isinstance(expr.operator.type, EQUAL_EQUAL):
            return self._isEqual(left,right)
        
        return None

    def _checkNumberOperand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        ######
        runtimeError("operand must be a number")

    

    def _checkNumberOperands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        runtimeError("operand must be a number")
        
        
        

    def _isEqual(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visitGroupingExpr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)