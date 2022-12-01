from plox.lexer.token import Token
HAD_ERROR = False
HAD_RUNTIME_ERROR = False


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}")
    HAD_ERROR = True


class PLoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token
        

def runtime_error(error: PLoxRuntimeError):
    print(f"[line {error.token.line}] {str(error)} \n")
    HAD_RUNTIME_ERROR = True

