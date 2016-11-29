type_int = 'integer'
type_bool = 'bool'
type_label = 'label'


def converter(type, value):
    if type == type_int:
        return int(value)
    if type == type_bool:
        if value == 'T':
            return True
        else:
            return False
    # TODO add functions


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
                cur_label = stmt.stmt.value
                self.labels.append(cur_label)
                self.blocks[cur_label] = []
            elif not cur_label:
                self.stmts.append(stmt)
            else:
                self.blocks[cur_label].append(stmt)

    def exec_statements(self, stmts, label):
        for stmt in stmts:
            res = stmt.exec()
            if isinstance(res, Label):
                print('GO TO -> label', res.value)
                return self.labels.index(res.value)
        return label + 1

    def exec(self):
        print('--Exec before labels--')
        label = self.exec_statements(self.stmts, -1)
        for i in range(label, len(self.labels)):
            label = self.labels[i]
            print('--Exec label--', label)
            stmts = self.blocks[label]
            self.exec_statements(stmts, i)


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def exec(self):
        return self.stmt.exec()


class GoTo(Node):
    def __init__(self, label):
        self.label = label

    def exec(self):
        return self.label


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
        # return converter(self.value_type, self.value)
        return self.value


class VarAssign(Node):
    def __init__(self, varL, varR):
        self.varL = varL
        self.varR = varR

    def exec(self):
        self.varL.value = self.varR.exec()
        print(self.varL.value_type + " " + self.varL.id + " : " + str(self.varL.value))
        return self.varL


class Expr(Node):
    def __init__(self, var, type, operator):
        self.var = var
        self.operator = operator
        self.type = type

    def exec(self):
        if self.operator == '--':
            print('---exec op decrement---')
            self.var.value = int(self.var.exec()) - 1
        if self.operator == '++':
            print('---exec op increment---')
            self.var.value = int(self.var.exec()) + 1
        return self.var.exec()


class Condition(Node):
    def __init__(self, value, literal):
        self.value = value
        self.literal = literal
        self.value_type = type_bool

    def exec(self):
        print('---exec condition ---')
        v = self.value.exec()
        l = self.literal.exec()
        if v == l:
            return 'T'
        else:
            return 'F'


class Literal(Node):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type

    def exec(self):
        # return converter(self.value_type, self.value)
        return self.value


class Empty(Node):
    def exec(self):
        pass
