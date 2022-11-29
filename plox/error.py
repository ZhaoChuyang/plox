HAD_ERROR = False

HAD_RUNTIME_ERROR = False

def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}")
    HAD_ERROR = True

"""
7.4.1
author: anhangcheng
2022.11.28 17:13
"""
##
def runtimeError(error: RuntimeError):
    print(f"{error}")
    HAD_RUNTIME_ERROR = True