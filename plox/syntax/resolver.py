from plox.syntax import Visitor
from plox.syntax.interpreter import *
from plox.syntax import stmt as STMT
from enum import Enum
# class Resolver implements Expr.Visitor<Void>, Stmt.Visitor<Void>
class FunctionType(Enum):
    NONE = 'none',
    FUNCTION = 'function' 

class Resolver(Visitor):
    interpreter: Interpreter
    #private final Stack<Map<String, Boolean>> scopes = new Stack<>();
    scopes = [dict()]

    current_function: FunctionType.NONE
    
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, stmt: STMT.Block):
        self.begin_scope()
        self.resolve(stmt.statement)
        self.end_scope()
        return None
    
    def visit_expression_stmt(self, stmt: STMT.Expression):
        self.resolve(stmt.expression)
        return None

    def visit_function_stmt(self, stmt: STMT.Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    def visit_if_stmt(self, stmt: STMT.If):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolve(stmt.elseBranch)
        return None
    
    def visit_print_stmt(self, stmt: stmt.Print):
        self.resolve(stmt.expression)
        return None

    def visit_return_stmt(self, stmt: stmt.Return):
        if self.current_function == FunctionType.NONE:
            error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            self.resolve(stmt.value)
        return None

    
    def visit_var_stmt(self, stmt: STMT.Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_while_stmt(self, stmt: STMT.While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_assign_expr(self, expr: EXPR.Assign):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)
        return None

    def visit_binary_expr(self, expr: EXPR.Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_call_expr(self, expr: EXPR.Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)
        
        return None
    
    def visit_grouping_expr(self, expr: EXPR.Grouping):
        self.resolve(expr.expression)
        return None
    
    def visit_literal_expr(self, expr: EXPR.Literal):
        return None
    
    def vsisit_logical_expr(self, expr: EXPR.Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_unary_expr(self, expr: EXPR.Unary):
        self.resolve(expr.right)
        return None



    def visit_variable_expr(self, expr: EXPR.Variable):
        ## !scopes.isempty()
        if self.scopes and isinstance(self.scopes[-1].get(expr.name.lexeme), False):
            error(expr.name,"Can't read local variable in its own initializer.")
        self.resolveLocal(expr, expr.name)
        return None

    
    def resolve(self, stmt: STMT.Stmt):
        stmt.accept(self)

    def resolve(self, expr: EXPR.Expr):
        expr.accept(self)

    def resolve(self, statements: list[STMT.Stmt]):
        for statement in statements:
            self.resolve(statement)
    
    def resolve_function(self, function: STMT.Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function



    def begin_scope(self):
        # scopes.push(new HashMap<String, Boolean>());
        self.scopes.append(dict())

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        # self.scopes.isEmpty()
        if not self.scopes:
            return
        scope = {}
        scope = self.scopes[-1]
        if scope.__contains__(name.lexeme):
            error(name,"Already a variable with this name in this scope.")

        scope[name.lexeme] = False
    
    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolveLocal(self, expr: EXPR.Expr, name: Token):
        for i in range(self.scopes.__sizeof__ -1 , -1):
            if self.scopes[i].__contains__(name.lexeme):
                self.interpreter.resolve(expr, self.scopes.__sizeof__ -1 -i)
                return