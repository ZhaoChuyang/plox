from plox.lexer.token import Token
HAD_ERROR = False
HAD_RUNTIME_ERROR = False


def error(line: int, message: str):
    if isinstance(line, Token):
        line = line.line
    report(line, "", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}")
    HAD_ERROR = True
    exit(1)


class PLoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token


def runtime_error(error: PLoxRuntimeError):
    print(error)
    HAD_ERROR = True
    HAD_RUNTIME_ERROR = True
