from plox.error import PLoxRuntimeError


class Environment:
    def __init__(self):
        values = {}
    
    def define(self, name: str, value: object) -> None:
        """
        binds the value to a specified variable name.
        """
        self.values[name] = value

    def get(self, name: str) -> object:
        if name in self.values:
            return self.values[name]
        
        raise PLoxRuntimeError(name, f"Variable {name} does not exist.")