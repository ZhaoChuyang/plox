from abc import ABC, abstractmethod
from expr import *
from plox.lexer.token import *
from decimal import Decimal
from error import *
import string
class Interpreter(implements=Visitor):

    def _interpret(self, expression: Expr) -> None:
        try:
            value = self._evaluate(expression)
            print(self._stringify(value)+"\n")
        except RuntimeError as e: 
            runtimeError(e)
            
    # catch (RuntimeError error) {
    #   Lox.runtimeError(error);
    # }
            

    def _stringify(self, object: object) -> string:
        if object == None :return "nil"
        if isinstance(object, float):
            text = string(object)
            if text.endswith(".0"):
                text = text[0, text.length-2]
            return text
        return string(object)

    def _visitLiteralExpr(self, expr: Literal) -> object:
        return expr.value

    def _isTruthy(self, object: object) -> bool:
        if object == None:
            return False
        if isinstance(object,bool):
            return bool(object)
        return True

    def _visitUnaryExpr(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)
        
        if expr.operator.type == MINUS:
            self._checkNumberOperand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == BANG:
            return self._isTruthy(right)

        return None


    
    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
    
    def _visitBinaryExpr(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        if expr.operator.type == GREATER:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == GREATER_EQUAL:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == LESS:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == LESS_EQUAL:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == MINUS:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, string) and isinstance(right, string):
                return string(left) + string(right)
        elif expr.operator.type == SLASH:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == STAR:
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == BANG_EQUAL:
            return not self._isEqual(left,right)
        elif expr.operator.type == EQUAL_EQUAL:
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
        if a == None and b == None:
            return True
        if a == None:
            return False
        return a==b

    def _visitGroupingExpr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)


