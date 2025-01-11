from tokenize import TokenType, Tokenizer

class AST(object):
    def __init__(self) -> None:
        pass


class Num:
    def __init__(self, token) -> None:
        self.type = token.type
        self.value = token.value

class BinOp:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right
        self.tree = None

class AstBuilder(AST):

    def __init__(self, tokens) -> None:
        self.position = 0
        self.tokens = tokens
        self.current_token = self.tokens[self.position] if len(self.tokens) > 0 else None
        self.nodes = []

    def eat(self, token_type):
        if token_type == self.current_token.type:
            self.position += 1
            self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        else:
            raise Exception(f"error parsing source at line {self.current_token.line}")

    def factor(self):
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(token.type)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise Exception(f"error parsing source at line {self.current_token.line}")


    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        
        return node

    def expr(self):
        node = self.term()
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def walk(self, node):
        if not node:
            return

        if type(node) == BinOp:
            self.walk(node.left)
            self.walk(node.right)
        else:
            print(node.value)

    def calculate(self, node):
        if not node:
            return None

        if type(node) == BinOp:
            left_val = self.calculate(node.left)
            right_val = self.calculate(node.right)
            if node.op.value == '+':
                return left_val + right_val if left_val and right_val else left_val or right_val
            if node.op.value == '-':
                return left_val - right_val if left_val and right_val else left_val or right_val
            if node.op.value == '*':
                return left_val * right_val if left_val and right_val else left_val or right_val
            if node.op.value == '/':
                return left_val / right_val if left_val and right_val else left_val or right_val
        elif type(node) == Num:
            return int(node.value)

    def build(self):
        while self.current_token is not None:
            self.nodes.append(self.expr())

        return self


"""
        *
       / \
      +   1
     / \
    2   3
"""
source = """
    2 + 2 + (3 + 4)
    1 * 2
    1 / 2
    1 + 2
    1 - 2
"""

t = Tokenizer(source)
t.tokenize()
builder = AstBuilder(t.tokens())
builder.build()

for node in builder.nodes:
    result = builder.calculate(node)
    print(result)
