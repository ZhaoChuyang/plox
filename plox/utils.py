import os
from typing import List, Union
from plox.syntax.stmt import Stmt
from plox.lexer.token import Token
from plox.syntax.expr import Expr


def check_path_exists(path: str):
    """
    Return true if the given path exists, false if not.
    """
    return os.path.exists(path)


def print_syntax_tree(name, node: Union[List[Stmt], Stmt], level_markers = [], marker_str = "+-"):
    # for root
    if isinstance(node, Token):
        name = node.type
        children = []
        names = []
    elif isinstance(node, List):
        names = [n.__class__.__name__ for n in node]
        children = node
        # print(children)
    elif isinstance(node, (Expr, Stmt)):
        names = []
        children = []
        for attr in dir(node):
            if not attr.startswith("_") and attr not in ["accept"] and getattr(node, attr) is not None:
                names.append(attr)
                children.append(getattr(node, attr))
        # from IPython import embed
        # embed()
        # print(names, children)
    else:
        children = []
        names = []
    
    # print(indent[:-3] + "|_" * bool(indent) + label)
    # print("\t" * int(level), name)
    empty_str = " " * len(marker_str)
    connection_str = "|" + empty_str[:-1]
    level = len(level_markers)
    mapper = lambda draw: connection_str if draw else empty_str
    markers = "".join(map(mapper, level_markers[:-1]))
    markers += marker_str if level > 0 else ""
    if isinstance(node, (Expr, Stmt)):
        name = node.__class__.__name__
    
    print(f"{markers}{name}")
    # from IPython import embed
    # embed()
    for i, (name, child) in enumerate(zip(names, children)):
        is_last = i == len(children) - 1
        print_syntax_tree(name, child, [*level_markers, not is_last])
