from tokenize import TokenType, Tokenizer

class Ast(object):
    def __init__(self) -> None:
        pass

class Num(Ast):
    def __init__(self, token) -> None:
        self.type = token.type
        self.value = token.value

class BinOp(Ast):
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right

"""
    factor -> int, (expr)
    term -> factor | * / factor
    expr -> term + - term

"""

class AstBuiler:
    def __init__(self, tokens) -> None:
        self.position = 0
        self.tokens = tokens
        self.current_token = self.tokens[self.position] if len(self.tokens) > 0 else None
        self.tree = None

    def eat(self, token):
        if token == self.current_token.type:
            self.position += 1
            self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        else:
            print(token, self.current_token.type)
            raise Exception(f"Error parsing source ({token.type} != {self.current_token.type})")

    def factor(self):
        #  print("fac = ", self.current_token.type, self.current_token.value)
        token = self.current_token
        if self.current_token.type == TokenType.INTEGER:
            self.eat(token.type)
            return Num(token)
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            pass

    def term(self):
        node = self.factor()
        #  print("term = ", node.type, node.value)
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node =  BinOp(left=node, op=token, right=self.factor())
        
        return node

    def expr(self):
        node = self.term()
        #  print("expr ", self.current_token.type)
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        
        return node

    def walk(self, node):
        if not node:
            return
        
        if type(node) == BinOp:
            self.walk(node.left)
            self.walk(node.op)
            self.walk(node.right)
        else:
            print(type(node), node.value)

    def build(self):
        self.tree = self.expr()


source = """
1 * (2 - (2 * 2 / 3));
"""

t = Tokenizer(source)
t.tokenize()

builder = AstBuiler(t.tokens())
builder.build()
builder.walk(builder.tree)
