class Node:
    def exec(self):
        raise NotImplementedError


class Statements(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def exec(self):
        for stmt in self.stmts:
            stmt.exec()


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def exec(self):
        self.stmt.exec()


class Var(Node):
    def __init__(self, id, value, value_type):
        self.id = id
        self.value = value
        self.value_type = value_type

    def exec(self):
        print(self.value_type + " " + self.id + " : " + str(self.value))


class VarAssign(Node):
    def __init__(self, varL, varR):
        self.varL = varL
        self.varR = varR

    def exec(self):
        self.varL.value = self.varR.value


class IntExpr(Node):
    def __init__(self, var, operator):
        self.var = var
        self.operator = operator

    def exec(self):
        if self.operator == '--':
            self.var.value = int(self.var.value) - 1
        if self.operator == '++':
            self.var.value = int(self.var.value) + 1
        self.var.exec()


class Literal(Node):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type

    def exec(self):
        print(self.value)
        return self.value

