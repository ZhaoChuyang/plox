import cmd
from plox.lexer import Scanner
from plox.syntax import Parser
from plox.syntax import Interpreter
from plox.utils import check_path_exists
from plox.error import HAD_ERROR, HAD_RUNTIME_ERROR


class PLoxPromt(cmd.Cmd):
    """
    Class of the interactive shell of PLox.
    """
    prompt = 'plox> '
    intro = ">>>>> PLox Interactive Shell <<<<<"

    def do_exit(self, inp):
        print("Bye")
        return True
    
    def default(self, line: str) -> None:
        if "exit()" in line:
            return self.do_exit(line)
        
        run(line)
        HAD_ERROR = False
        
    do_EOF = do_exit


def run_script(path: str):
    assert check_path_exists(path), f"Script file: {path} was not found."
    with open(path, "r") as fb:
        script = "\n".join(fb.readlines())
        run(script)
    
    if HAD_ERROR: exit(1)
    if HAD_RUNTIME_ERROR: exit(2)
    exit(0)


def run_promt():
    promt = PLoxPromt()
    promt.cmdloop()


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    print(tokens)
    parser = Parser(tokens)
    statements = parser.parse()
    print(statements)
    interpreter = Interpreter()
    interpreter.interpret(statements)
