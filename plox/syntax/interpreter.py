from plox.syntax import Visitor
from plox.syntax import expr as EXPR
from plox.syntax import stmt as STMT
from plox.lexer.token import *
from plox.error import *
from enviroment import Environment


class Interpreter(Visitor):
    def __init__(self, environment: Environment):
        self.environment = environment

    def interpret(self, statements) -> None:
        try: 
            for statement in statements:
                self._execute(statement)
        except PLoxRuntimeError as e:
            runtime_error(e)

    def _execute(self, stmt: STMT.Stmt):
        stmt.accept(self)

    def visitBlockStmt(self, stmt: STMT.Block):
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

    def _stringify(self, object: object) -> str:
        if object is None :return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[:len(text)-2]
            return text
        return str(object)

    def visitLiteralExpr(self, expr: EXPR.Literal) -> object:
        return expr.value
    
    """
    new 
    new in ch9
    """
    def visitLogicalExpr(self, expr: EXPR.Logical):
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

    def visitUnaryExpr(self, expr: EXPR.Unary) -> object:
        right = self._evaluate(expr.right)
        
        if isinstance(expr.operator.type, MINUS):
            self._checkNumberOperand(expr.operator, right)
            return -float(right)
        elif isinstance(expr.operator.type, BANG):
            return self._isTruthy(right)

        return None

    def visitVariableExpr(self, expr: EXPR.Variable):
        return self.environment.get(expr.name)
    
    def _evaluate(self, expr: EXPR.Expr) -> object:
        return expr.accept(self)
    
    """
    new in 8.1.3
    """
    def visitExpressionStmt(self, stmt: STMT.Expression) -> None:
        """
        Syntax:
            exprStmt := expression ";" ;
        """
        self._evaluate(stmt.expression)
    
    def visitPrintStmt(self, stmt: STMT.Print):
        """
        Syntax:
            printStmt := "print" expression ";" ;
        """
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
    
    def visitVarStmt(self, stmt: STMT.Var):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)

    def visitAssignExpr(self, expr: EXPR.Assign) -> object:
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    """
    new in ch9
    """
    def visitIfStmt(self, stmt: STMT.If):
        if self._isTruthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self._execute(stmt.elseBranch)
        return None

    def visitBinaryExpr(self, expr: STMT.Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if isinstance(expr.operator, GREATER):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        elif isinstance(expr.operator, GREATER_EQUAL):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        elif isinstance(expr.operator, LESS):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        elif isinstance(expr.operator, LESS_EQUAL):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)
        elif isinstance(expr.operator, MINUS):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif isinstance(expr.operator, PLUS):
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        elif isinstance(expr.operator, SLASH):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        elif isinstance(expr.operator, STAR):
            self._checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        elif isinstance(expr.operator, BANG_EQUAL):
            return not self._isEqual(left,right)
        elif isinstance(expr.operator, EQUAL_EQUAL):
            return self._isEqual(left,right)
        
        return None

    def _checkNumberOperand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def _checkNumberOperands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def _isEqual(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visitGroupingExpr(self, expr: EXPR.Grouping) -> object:
        return self._evaluate(expr.expression)