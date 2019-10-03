import operator

class Symbol:
    pass


class Variable(Symbol):
    def __init__(self, string):
        """Represents a variable"""
        self.string = string


class Constant(Symbol):
    def __init__(self, value):
        self.value = value


class Operator(Symbol):
    def __init__(self, operands=2):
        self.operands = operands


class And(Operator):
    operator = operator.and_
    pass


class Or(Operator):
    pass


class Not(Operator):
    def __init__(self):
        super().__init__(self, operands=1)
