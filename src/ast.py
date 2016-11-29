class Node:
    def exec(self):
        raise NotImplementedError


class Statements(Node):
    def __init__(self, stmts):
        self.stmts = []
        self.blocks = {}
        self.labels = []
        self.build_tree(stmts)

    def build_tree(self, stmts):
        cur_label = None
        for stmt in stmts:
            if isinstance(stmt.stmt, Empty):
                pass
            elif isinstance(stmt.stmt, Label):
                cur_label = stmt.stmt
                self.labels.append(cur_label)
                self.blocks[cur_label] = []
            elif not cur_label:
                self.stmts.append(stmt)
            else:
                self.blocks[cur_label].append(stmt)

    def exec(self):
        print('--Exec before labels--')
        for stmt in self.stmts:
            stmt.exec()

        for label in self.labels:
            print('--Exec label--', label.value)
            stmts = self.blocks[label]
            for stmt in stmts:
                stmt.exec()


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def exec(self):
        self.stmt.exec()


class GoTo(Node):
    def __init__(self, label):
        self.label = label

    def exec(self):
        return self.label, 'go_to'


class Label(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        return self.value


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
        print(self.varL.value_type + " " + self.varL.id + " : " + str(self.varL.value))


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


class Empty(Node):
    def exec(self):
        pass
