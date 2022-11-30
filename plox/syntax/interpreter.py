from plox.syntax import Visitor
from plox.syntax import expr as EXPR
from plox.syntax import stmt as STMT
from plox.lexer.token import *
from plox.error import *
from plox.syntax.enviroment import Environment


class Interpreter(Visitor):
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements) -> None:
        try: 
            for statement in statements:
                self._execute(statement)
        except PLoxRuntimeError as e:
            runtime_error(e)

    def _execute(self, stmt: STMT.Stmt):
        stmt.accept(self)

    def visitBlockStmt(self, stmt: STMT.Block):
        self.execute_block(stmt.statements, Environment(self.environment))
    
    def execute_block(self, statements, environment: Environment):
        # original enviroment outside the block
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            # after leaving this block, delete related environment,
            # i.e. restore to the original environment
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
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def _is_truthy(self, object: object) -> bool:
        if object is None:
            return False
        if isinstance(object,bool):
            return bool(object)
        return True

    def visitUnaryExpr(self, expr: EXPR.Unary) -> object:
        right = self._evaluate(expr.right)
        
        if isinstance(expr.operator.type, MINUS):
            self._check_number_operand(expr.operator, right)
            return -float(right)
        elif isinstance(expr.operator.type, BANG):
            return self._is_truthy(right)

        return None

    def visitVariableExpr(self, expr: EXPR.Variable):
        # the type of expr.name is Token, you need to access its attribute lexeme to get the true variable name.
        return self.environment.get(expr.name.lexeme)
    
    def _evaluate(self, expr: EXPR.Expr) -> object:
        """
        `_evaluate()` is used specifically for Expression, which allows the given expr evaluate
        itself with the appropriate visitor method. For every Expression defined in `expr.py`
        you need to provide a visitor method to evaluate and return the expected value for interpreting.
        
        Note: Statement is evaluated using the `_execute()` method.
        """
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
    
    """
     new in 9.2
    """
    def visitIfStmt(self, stmt: STMT.If):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self._execute(stmt.elseBranch)
        return None

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
    """
         new in 9
    """
    def visitWhileStmt(self, stmt: STMT.While):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)
        return None

    def visitAssignExpr(self, expr: EXPR.Assign) -> object:
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    """
    new in ch9
    """
    def visitIfStmt(self, stmt: STMT.If):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self._execute(stmt.elseBranch)
        return None

    def visitBinaryExpr(self, expr: EXPR.Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if isinstance(expr.operator, GREATER):
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif isinstance(expr.operator, GREATER_EQUAL):
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif isinstance(expr.operator, LESS):
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif isinstance(expr.operator, LESS_EQUAL):
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif isinstance(expr.operator, MINUS):
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif isinstance(expr.operator, PLUS):
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        elif isinstance(expr.operator, SLASH):
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif isinstance(expr.operator, STAR):
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif isinstance(expr.operator, BANG_EQUAL):
            return not self._is_equal(left,right)
        elif isinstance(expr.operator, EQUAL_EQUAL):
            return self._is_equal(left,right)
        
        return None

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def _check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def _is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visitGroupingExpr(self, expr: EXPR.Grouping) -> object:
        return self._evaluate(expr.expression)