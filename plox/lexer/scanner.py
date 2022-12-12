from typing import List
from plox.lexer.token import *
from plox.error import error


class Scanner:
    def __init__(self):
        self.source = None
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "and": AND,
            "class": CLASS,
            "else": ELSE,
            "false": FALSE,
            "for": FOR,
            "fun": FUN,
            "if": IF,
            "nil": NIL,
            "or": OR,
            "print": PRINT,
            "return": RETURN,
            "super": SUPER,
            "this": THIS,
            "true": TRUE,
            "var": VAR,
            "while": WHILE,
            "lambda": LAMBDA
        }
    
    def _is_end(self) -> bool:
        return self.current >= len(self.source)
    
    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected: str) -> bool:
        """
        Check whether the next character, i.e. source[current], matchs character `expected`.
        If matches, advance one step, return True. Otherwise directly return False.
        """
        if self._is_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def _peek(self, n=1) -> str:
        """
        Get the next n character, i.e. source[current+n-1], without advancing `current` pointer.
        If the character to peek exceed the end of the source file, return None.

        Args:
            n (int): peek the n-th next character. By default peek the next character.
        """
        if self.current + n - 1 >= len(self.source): return None
        return self.source[self.current + n - 1]

    def _is_digit(self, c) -> bool:
        """
        Check whether the input character c is a digit number.
        """
        return ord(c) >= ord('0') and ord(c) <= ord('9')

    def _number(self) -> None:
        """
        Process the number literal. Add the NUMBER token.
        """
        while not self._is_end() and self._is_digit(self._peek()):
            self._advance()
        
        # look for a fractional part
        if self._peek() == '.' and self._is_digit(self._peek(2)):
            # consume the '.'
            self._advance()
            
            while self._is_digit(self._peek()):
                self._advance()
        
        self._add_token(
            NUMBER(self.source[self.start:self.current], float(self.source[self.start:self.current]), self.line))

    def _string(self) -> None:
        """
        Process string literal. Add the STRING token with its literal being trimed string surrounding by the quotes.
        """
        while (not self._is_end() and self._peek() != '"'):
            if self._peek() == '\n': self.line += 1
            self._advance()
        
        if self._is_end():
            error(self.line, "Unterminated string.")
            return
        
        # in case the current character is the closing ", we consume it and return the trimed string in the surrounding quotes.
        self._advance()

        # after advancing, source[current-1] is ", source[start+1..current-2] is the trimed string.
        value = self.source[self.start+1:self.current-1]
        self._add_token(STRING(self.source[self.start:self.current], value, self.line))

    def _is_alpha(self, c: str) -> bool:
        """
        Check if character c is a valid identifier leading character.
        Any lexme starting with letters or underscore is a valid identifier.
        """
        return (ord(c) >= ord('a') and ord(c) <= ord('z')) or (ord(c) >= ord('A') and ord(c) <= ord('Z')) or c == '_'

    def _is_alpha_numeric(self, c: str) -> bool:
        """
        Check if character c is a alphabet letter or numeric digit.
        """
        return self._is_alpha(c) or self._is_digit(c)

    def _identifier(self) -> None:
        """
        Process identifier and reserved keywords.
        Find the longest continuous lexeme from current position, then firstly try to find the matched reserved
        word from the predefined `keywords` dict, if no matched reserved word was found, add the lexeme as IDENTIFIER.
        """
        while not self._is_end() and self._is_alpha_numeric(self._peek()):
            self._advance()
        
        text = self.source[self.start:self.current]
        if text in self.keywords:
            self._add_token(self.keywords[text](self.source[self.start:self.current], None, self.line))
        else:
            self._add_token(IDENTIFIER(self.source[self.start:self.current], None, self.line))
        
    def _scan_token(self) -> None:
        c = self._advance()
        
        lexeme = self.source[self.start:self.current]
        line = self.line
        literal = None

        # single-character token
        if c == '(': self._add_token(LEFT_PAREN(lexeme, literal, line))
        elif c == ')': self._add_token(RIGHT_PAREN(lexeme, literal, line))
        elif c == '{': self._add_token(LEFT_BRACE(lexeme, literal, line))
        elif c == '}': self._add_token(RIGHT_BRACE(lexeme, literal, line))
        elif c == ',': self._add_token(COMMA(lexeme, literal, line))
        elif c == '.': self._add_token(DOT(lexeme, literal, line))
        elif c == '-': self._add_token(MINUS(lexeme, literal, line))
        elif c == '+': self._add_token(PLUS(lexeme, literal, line))
        elif c == ';': self._add_token(SEMICOLON(lexeme, literal, line))
        elif c == '*': self._add_token(STAR(lexeme, literal, line))
        elif c == ':': self._add_token(COLON(lexeme, literal, line))
        # two-characters token
        elif c == '!':
            self._add_token(BANG_EQUAL(lexeme, literal, line) if self._match("=") else BANG(lexeme, literal, line))
        elif c == '=':
            self._add_token(EQUAL_EQUAL(lexeme, literal, line) if self._match("=") else EQUAL(lexeme, literal, line))
        elif c == '<':
            self._add_token(LESS_EQUAL(lexeme, literal, line) if self._match("=") else LESS(lexeme, literal, line))
        elif c == '>':
            self._add_token(GREATER_EQUAL(lexeme, literal, line) if self._match("=") else GREATER(lexeme, literal, line))
        # process for '/' which can be either division operator or the start of the comment
        elif c == '/':
            if self._match('/'):
                while self._peek() != '\n' and not self._is_end():
                    self._advance()
            else:
                self._add_token(SLASH(lexeme, literal, line))
        # ignore white spaces
        elif c in [' ', '\r', '\t']:
            pass
        # advance to the next line, incrementing the line counter
        elif c == '\n':
            self.line += 1
        # process string literal
        elif c == '"':
            self._string()
        # process number literal
        elif self._is_digit(c):
            self._number()
        # process identifier and reserved word
        elif self._is_alpha(c):
            self._identifier()
        else:
            error(line, "Unexpected character.")

    def _add_token(self, token: Token) -> None:
        self.tokens.append(token)

    def scan_tokens(self, source: str) -> List[Token]:
        self.source = source
        while not self._is_end():
            self.start = self.current
            self._scan_token()
        
        self.tokens.append(EOF("", None, self.line))
        return self.tokens
