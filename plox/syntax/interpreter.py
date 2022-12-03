from plox.syntax import Visitor
from plox.syntax import expr as EXPR
from plox.syntax import stmt as STMT
from plox.lexer.token import *
from plox.error import runtime_error, PLoxRuntimeError
from plox.syntax.environment import Environment
from plox.syntax.loxcallable import Clock, LoxCallable
from plox.syntax.loxfunction import *
from plox.syntax.ret import Return


class Interpreter(Visitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define("clock", Clock())
        self.locals = {}

    def interpret(self, statements) -> None:
        try: 
            for statement in statements:
                self.execute(statement)
        except PLoxRuntimeError as e:
            runtime_error(e)

    def execute(self, stmt: STMT.Stmt):
        stmt.accept(self)
    
    def resolve(self, expr: EXPR.Expr, depth: int):
        self.locals[expr] = depth

    def visitBlockStmt(self, stmt: STMT.Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def execute_block(self, statements, environment: Environment):
        # original enviroment outside the block
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            # after leaving this block, delete related environment,
            # i.e. restore to the original environment
            self.environment = previous

    def stringify(self, object: object) -> str:
        if object is None :return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[:len(text)-2]
            return text
        return str(object)

    def visitLiteralExpr(self, expr: EXPR.Literal) -> object:
        return expr.value
    
    def visitLogicalExpr(self, expr: EXPR.Logical):
        left = self.evaluate(expr.left)
        if isinstance(expr.operator.type, OR):
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

    def is_truthy(self, object: object) -> bool:
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def visitUnaryExpr(self, expr: EXPR.Unary) -> object:
        right = self.evaluate(expr.right)
        
        if isinstance(expr.operator.type, MINUS):
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif isinstance(expr.operator.type, BANG):
            return self.is_truthy(right)

        return None

    def visitVariableExpr(self, expr: EXPR.Variable):
        # the type of expr.name is Token, you need to access its attribute lexeme to get the true variable name.
        return self.lookup_variable(expr.name, expr)

    def lookup_variable(self, name: Token, expr: EXPR.Expr):
        distance = self.locals.get(expr, None)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name.lexeme)
    
    def evaluate(self, expr: EXPR.Expr) -> object:
        """
        `_evaluate()` is used specifically for Expression, which allows the given expr evaluate
        itself with the appropriate visitor method. For every Expression defined in `expr.py`
        you need to provide a visitor method to evaluate and return the expected value for interpreting.
        
        Note: Statement is evaluated using the `_execute()` method.
        """
        return expr.accept(self)
    
    def visitExpressionStmt(self, stmt: STMT.Expression) -> None:
        """
        Syntax:
            exprStmt := expression ";" ;
        """
        self.evaluate(stmt.expression)

    def visitFunctionStmt(self, stmt: STMT.Function):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
    
    def visitIfStmt(self, stmt: STMT.If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visitPrintStmt(self, stmt: STMT.Print):
        """
        Syntax:
            printStmt := "print" expression ";" ;
        """
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
    
    def visitReturnStmt(self, stmt: STMT.Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visitVarStmt(self, stmt: STMT.Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)

    def visitWhileStmt(self, stmt: STMT.While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitAssignExpr(self, expr: EXPR.Assign) -> object:
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr, None)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visitIfStmt(self, stmt: STMT.If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visitBinaryExpr(self, expr: EXPR.Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if isinstance(expr.operator, GREATER):
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif isinstance(expr.operator, GREATER_EQUAL):
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif isinstance(expr.operator, LESS):
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif isinstance(expr.operator, LESS_EQUAL):
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif isinstance(expr.operator, MINUS):
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif isinstance(expr.operator, PLUS):
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        elif isinstance(expr.operator, SLASH):
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif isinstance(expr.operator, STAR):
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif isinstance(expr.operator, BANG_EQUAL):
            return not self.is_equal(left,right)
        elif isinstance(expr.operator, EQUAL_EQUAL):
            return self.is_equal(left,right)
        
        return None

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise PLoxRuntimeError(operator, "operand must be a number")

    def is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visitGroupingExpr(self, expr: EXPR.Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitCallExpr(self, expr: EXPR.Call):
        # expr.callee is an instance of Expr. More specifically a Variable
        # if expr.callee is a valid identifier. The variable refering to
        # the function name will finally be evaluated to the function object itself.
        callee = self.evaluate(expr.callee)
        
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, LoxCallable):
            raise PLoxRuntimeError(expr.paren, "Can only call functions and classes.")
        
        function = callee
        
        if len(arguments) != function.arity():
            raise PLoxRuntimeError(expr.paren,
                f"Expected {function.arity()} arguments but got {arguments.size()}.")

        return function.call(self, arguments)


    