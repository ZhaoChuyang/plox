import enum
from typing import List, Union
from plox.syntax import Visitor
from plox.syntax.interpreter import Interpreter
from plox.syntax import stmt as STMT
from plox.syntax import expr as EXPR
from plox.lexer.token import Token
from plox.error import PLoxRuntimeError, error


class FunctionType(enum.Enum):
    NONE = 0
    FUNCTION = 1
    INITIALIZER = 2
    METHOD = 3


class ClassType(enum.Enum):
    NONE = 0
    CLASS = 1
    SUBCLASS = 2


class Resolver(Visitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def visitBlockStmt(self, stmt: STMT.Block) -> None:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
    
    def visitExpressionStmt(self, stmt: STMT.Expression) -> None:
        self.resolve(stmt.expression)

    def visitFunctionStmt(self, stmt: STMT.Function) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
    
    def visitIfStmt(self, stmt: STMT.If) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)
    
    def visitPrintStmt(self, stmt: STMT.Print) -> None:
        self.resolve(stmt.expression)

    def visitReturnStmt(self, stmt: STMT.Return) -> None:
        if self.current_function == FunctionType.NONE:
            PLoxRuntimeError(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function is FunctionType.INITIALIZER:
                error(stmt.keyword, "Can't return a value from an initializer.")
            
            self.resolve(stmt.value)
    
    def visitVarStmt(self, stmt: STMT.Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
    
    def visitWhileStmt(self, stmt: STMT.While) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visitAssignExpr(self, expr: EXPR.Assign) -> None:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visitBinaryExpr(self, expr: EXPR.Binary) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)
    
    def visitCallExpr(self, expr: EXPR.Call) -> None:
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)
    
    def visitGroupingExpr(self, expr: EXPR.Grouping) -> None:
        self.resolve(expr.expression)
    
    def visitLiteralExpr(self, expr: EXPR.Literal) -> None:
        pass
    
    def vsisitLogicalExpr(self, expr: EXPR.Logical) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnaryExpr(self, expr: EXPR.Unary) -> None:
        self.resolve(expr.right)

    def visitVariableExpr(self, expr: EXPR.Variable) -> None:
        """
        Variable Evaluation.
        """
        # we don't allow initilize a undefined variable
        if self.scopes and self.scopes[-1].get(expr.name.lexeme, None) is False:
            PLoxRuntimeError(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)

    def visitClassStmt(self, stmt: STMT.Class) -> None:
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                error(stmt.superclass.name, "A class can't inherit from itself.")
            
            self.current_class = ClassType.SUBCLASS
            self.resolve(stmt.superclass)
            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == 'init':
                declaration = FunctionType.INITIALIZER
            self.resolve_function(method, declaration)
        
        self.end_scope()

        if stmt.superclass is not None:
            self.end_scope()

        self.current_class = enclosing_class
        
    
    def resolve_local(self, expr: EXPR.Expr, name: Token) -> None:
        # resolve the variable to evaluate to its nearest definition in the static stage.
        for i in range(len(self.scopes)-1 , -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes)-1-i)
                return

    def resolve(self, syntax: Union[STMT.Stmt, EXPR.Expr, List[STMT.Stmt]]):
        # for block statements list
        if isinstance(syntax, List):
            for statement in syntax:
                self.resolve(statement)
            return
        
        # for regular expression and statement, using the corresponding visitor function to resolve itself.
        syntax.accept(self)
    
    def resolve_function(self, function: STMT.Function, func_type: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = func_type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append(dict())

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        # for variable defined in global scope, we don't track it.
        if not self.scopes: return
        
        scope = self.scopes[-1]
        if name.lexeme in scope:
            raise PLoxRuntimeError("Already a variable with this name in this scope.")
        scope[name.lexeme] = False
    
    def define(self, name: Token) -> None:
        # for variable defined in global scope, we don't track it.
        if not self.scopes: return
        self.scopes[-1][name.lexeme] = True

    def visitGetExpr(self, expr: EXPR.Get) -> None:
        object = self.resolve(expr.object)
    
    def visitSetExpr(self, expr: EXPR.Set) -> None:
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visitSuperExpr(self, expr: EXPR.Super) -> None:
        if self.current_class is ClassType.NONE:
            error(expr.keyword.line, "Can't use 'super' outside of a class.")
        elif self.current_class is not  ClassType.SUBCLASS:
            error(expr.keyword.line, "Can't use 'super' in a class with no superclass.")

        self.resolve_local(expr, expr.keyword)

    def visitThisExpr(self, expr: EXPR.This) -> None:
        if self.current_class is not ClassType.CLASS:
            error(expr.keyword, "Can't use 'this'  outside of the class definition.")

        self.resolve_local(expr, expr.keyword)
