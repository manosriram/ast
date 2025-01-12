import ast

source = """
x = 123
y = 234
print(x+y)
while 2 == 2 and 2 == 2:
    continue
"""

CONSTANT_WHILE_CONDITION = "Constant value in while condition"
CONDITION_ALWAYS_TRUE = "Condition always results to True"

class While:
    def __init__(self, node) -> None:
        self.node = node
        self.checks = []

    def check_comparator(self, node):
        if type(node.test.left) == ast.Constant and type(node.test.comparators[0]) == ast.Constant:
            self.checks.append({ "check": CONDITION_ALWAYS_TRUE, "line": node.lineno })
            return False

    def check_boolop(self, node):
        ok = True
        before = len(self.checks)
        for node in node.test.values:
            print("node ", node)
            ok &= before != len(self.check(node).checks)

        return ok
     
    def check_constant(self, node):
        self.checks.append({ "check": CONSTANT_WHILE_CONDITION, "line": node.lineno })
        return False

    def check(self, node):
        print(node.__dict__)
        if type(node.test) == ast.Constant:
            self.check_constant(node)
        elif type(node) == ast.Compare:
            self.check_comparator(node)
        elif type(node.test) == ast.BoolOp:
            self.check_boolop(node)

        return self

class Checker:
    def __init__(self, source) -> None:
        self.source = source
        self.tree = ast.parse(source)
        self.checks = []

    def check(self):
        for x in self.tree.body:
            if type(x) == ast.While:
                self.checks.extend(While(x).check(x).checks)

        return self
                    
print(Checker(source).check().checks)
