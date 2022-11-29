import cmd
from plox.lexer import Scanner
from plox.syntax import Parser
from plox.utils import check_path_exists
from plox.error import HAD_ERROR


"""
7.4.1
author: anhangcheng
2022.11.28 17:13
"""
## new here
from plox.error import HAD_RUNTIME_ERROR
from main import interpreter

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

    """
    7.4.1
    author: anhangcheng
    2022.11.28 17:13
    """
    ### new here
    if HAD_RUNTIME_ERROR: exit(2)
    exit(0)


def run_promt():
    promt = PLoxPromt()
    promt.cmdloop()


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)


    for token in tokens:
        print(token)
    
    print(parser.parse())

    ## new here
    """
    7.4.1
    8.
    author: anhangcheng
    2022.11.28 17:13
    """
    statements = parser.parse()
    interpreter._interpret(statements)

