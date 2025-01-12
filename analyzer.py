import ast

source = """
x = 123
y = 234
print(x+y)
while 2 == 2:
    continue
"""

CONSTANT_WHILE_CONDITION = "Constant value in while condition"
CONDITION_ALWAYS_TRUE = "Condition always results to True"

class While:
    def __init__(self, node) -> None:
        self.node = node
        self.checks = []

    def check_comparator(self):
        if type(self.node.test.left) == ast.Constant and type(self.node.test.comparators[0]) == ast.Constant:
            self.checks.append({ "check": CONDITION_ALWAYS_TRUE, "line": self.node.lineno })
            return False

    def check_boolop(self):
        ok = True
        #  for node in self.node.test.values:
            #  ok &= self
            #  ok &= self.check_comparator()

    def check_constant(self):
        self.checks.append({ "check": CONSTANT_WHILE_CONDITION, "line": self.node.lineno })
        return False

    def check(self):
        if type(self.node.test) == ast.Constant:
            self.check_constant()
        if type(self.node.test) == ast.Compare:
            self.check_comparator()
        if type(self.node.test) == ast.BoolOp:
            self.check_boolop()

        return len(self.checks) == 0, self.checks

class Checker:
    def __init__(self, source) -> None:
        self.source = source
        self.tree = ast.parse(source)
        self.checks = []

    def check(self):
        for x in self.tree.body:
            if type(x) == ast.While:
                ok, errors = While(x).check()
                if not ok:
                    self.checks.extend(errors)

        return self
                    
print(Checker(source).check().checks)
