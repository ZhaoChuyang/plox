from typing import List, Dict
from plox.syntax.loxfunction import LoxFunction
from plox.syntax.loxcallable import LoxCallable



class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass, methods: Dict[str, LoxFunction]):
        self.superclass = superclass
        self.name = name
        self.methods = methods
    
    def find_function(self, name: str):
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.find_function(name)
        
        return None

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
