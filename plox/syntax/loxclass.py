from typing import List, Dict
from plox.syntax.loxfunction import LoxFunction
from plox.syntax.loxcallable import LoxCallable



class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods
    
    def find_function(self, name: str):
        return self.methods.get(name, None)

    def call(self, interpreter, arguments: List[object]):
        from plox.syntax.loxinstance import LoxInstance
        instance = LoxInstance(self)
        
        initializer = self.find_function("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        
        return instance

    def arity(self):
        initializer = self.find_function("init")
        if initializer is None: return 0
        return initializer.arity()

    def __repr__(self):
        return self.name
