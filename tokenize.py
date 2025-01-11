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
    def __init__(self, typ: TokenType, value) -> None:
        self.type = typ
        self.value = value

class Tokenizer:
    def __init__(self, source) -> None:
        self._source = source
        self._tokens = []
        self._position = 0

    def eat(self):
        self._position += 1

    def tokenize(self):
        while self._position < len(self._source):
            if self._source[self._position] in SKIP_TOKENS:
                self.eat()
            elif self._source[self._position] in [TokenType.PLUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MINUS, TokenType.LPAREN, TokenType.RPAREN]:
                self._tokens.append(Token(TokenType(self._source[self._position]), self._source[self._position]))
                self.eat()
            elif self._source[self._position].isdigit():
                f = self._position
                l = self._position
                while self._position < len(self._source) and self._source[self._position].isdigit():
                    l += 1
                    self.eat()
                self._tokens.append(Token(typ=TokenType.INTEGER, value=self._source[f:l]))
            elif self._source[self._position] == TokenType.SEMICOLON:
                self._tokens.append(Token(typ=TokenType.SEMICOLON, value=TokenType.SEMICOLON.value))
                self.eat()
            elif self._source[self._position] == TokenType.ASSIGN:
                self._tokens.append(Token(typ=TokenType.ASSIGN, value=TokenType.ASSIGN.value))
                self.eat()
            elif self._position < len(self._source):
                f = self._position
                l = self._position
                while self._position < len(self._source) and self._source[self._position] not in SKIP_TOKENS:
                    l += 1
                    self.eat()
                self._tokens.append(Token(typ=TokenType.VAR, value=self._source[f:l-1]))
                self.eat()

        #  self._tokens.append(Token(typ=TokenType.EOF, value=TokenType.EOF.value))

    def tokens(self):
        return self._tokens


#  source = """
    #  a = 123 + 211;
    #  c = a + ba;
#  """

#  tokenizer = Tokenizer(source)
#  tokenizer.tokenize()
#  print(tokenizer.tokens())

