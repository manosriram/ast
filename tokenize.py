from enum import Enum

SKIP_TOKENS = [" ", "\n"]

class TokenType(str, Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    ASSIGN = "="

    INTEGER = "int"
    VAR = "var"
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"

    EOF = "eof"


class Token:
    def __init__(self, typ: TokenType, value, line) -> None:
        self.type = typ
        self.value = value
        self.line = line

    def __str__(self) -> str:
        return f"{self.type}:{self.value}"

class Tokenizer:
    def __init__(self, source) -> None:
        self.source = source
        self.line = 0
        self.position = 0
        self._tokens = []

    def eat(self, line=False):
        self.position += 1
        if line:
            self.line += 1

    def tokenize(self):
        while self.position < len(self.source):
            if self.source[self.position] in SKIP_TOKENS:
                self.eat(line=self.source[self.position] == "\n")
            elif self.source[self.position] in [TokenType.PLUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MINUS, TokenType.LPAREN, TokenType.RPAREN]:
                self._tokens.append(Token(TokenType(self.source[self.position]), self.source[self.position], line=self.line))
                self.eat()
            elif self.source[self.position].isdigit():
                f = self.position
                l = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    l += 1
                    self.eat()
                self._tokens.append(Token(typ=TokenType.INTEGER, value=self.source[f:l], line=self.line))
            elif self.source[self.position] == TokenType.SEMICOLON:
                self._tokens.append(Token(typ=TokenType.SEMICOLON, value=TokenType.SEMICOLON.value, line=self.line))
                self.eat()
            elif self.source[self.position] == TokenType.ASSIGN:
                self._tokens.append(Token(typ=TokenType.ASSIGN, value=TokenType.ASSIGN.value, line=self.line))
                self.eat()
            elif self.position < len(self.source):
                f = self.position
                l = self.position
                while self.position < len(self.source) and self.source[self.position] not in SKIP_TOKENS:
                    l += 1
                    self.eat()
                self._tokens.append(Token(typ=TokenType.VAR, value=self.source[f:l-1], line=self.line))
                self.eat()

        return self

    def tokens(self):
        return self._tokens
