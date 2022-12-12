class Token:
    """
    Base class for all tokens
    """
    def __init__(self, type: str, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

"""
Single-character tokens
"""

class LEFT_PAREN(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("LEFT_PAREN", lexeme, literal, line)


class RIGHT_PAREN(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("RIGHT_PAREN", lexeme, literal, line)


class LEFT_BRACE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("LEFT_BRACE", lexeme, literal, line)


class RIGHT_BRACE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("RIGHT_BRACE", lexeme, literal, line)


class COMMA(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("COMMA", lexeme, literal, line)


class DOT(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("DOT", lexeme, literal, line)


class MINUS(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("MINUS", lexeme, literal, line)


class PLUS(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("PLUS", lexeme, literal, line)


class SEMICOLON(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("SEMICOLON", lexeme, literal, line)


class SLASH(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("SLASH", lexeme, literal, line)


class STAR(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("STAR", lexeme, literal, line)

"""
One or two character tokens
"""

class BANG(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("BANG", lexeme, literal, line)


class BANG_EQUAL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("BANG_EQUAL", lexeme, literal, line)


class EQUAL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("EQUAL", lexeme, literal, line)


class EQUAL_EQUAL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("EQUAL_EQUAL", lexeme, literal, line)


class GREATER(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("GREATER", lexeme, literal, line)


class GREATER_EQUAL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("GREATER_EQUAL", lexeme, literal, line)


class LESS(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("LESS", lexeme, literal, line)


class LESS_EQUAL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("LESS_EQUAL", lexeme, literal, line)

"""
Literals
"""

class IDENTIFIER(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("IDENTIFIER", lexeme, literal, line)


class STRING(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("STRING", lexeme, literal, line)


class NUMBER(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("NUMBER", lexeme, literal, line)

"""
Keywords
"""

class AND(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("AND", lexeme, literal, line)


class CLASS(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("CLASS", lexeme, literal, line)


class ELSE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("ELSE", lexeme, literal, line)


class FALSE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("FALSE", lexeme, literal, line)


class FUN(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("FUN", lexeme, literal, line)


class FOR(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("FOR", lexeme, literal, line)


class IF(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("IF", lexeme, literal, line)


class NIL(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("NIL", lexeme, literal, line)


class OR(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("OR", lexeme, literal, line)


class PRINT(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("PRINT", lexeme, literal, line)


class RETURN(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("RETURN", lexeme, literal, line)


class SUPER(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("SUPER", lexeme, literal, line)


class THIS(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("THIS", lexeme, literal, line)


class TRUE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("TRUE", lexeme, literal, line)


class VAR(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("VAR", lexeme, literal, line)


class WHILE(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("WHILE", lexeme, literal, line)


class LAMBDA(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("LAMBDA", lexeme, literal, line)


class COLON(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("COLON", lexeme, literal, line)

"""
EOF
"""

class EOF(Token):
    def __init__(self, lexeme: str, literal: object, line: int):
        super().__init__("EOF", lexeme, literal, line)
