type_int = 'integer'
type_bool = 'bool'
type_label = 'label'


class Node:
    def exec(self):
        raise NotImplementedError


class TypedItem(Node):
    def __init__(self, type):
        self.value_type = type

    def exec(self):
        raise NotImplementedError


class ValueItem(TypedItem):
    def __init__(self, value, type):
        super().__init__(type)
        self.value = value

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
        i = self.exec_statements(self.stmts, -1)
        while i < len(self.labels):
            label_id = self.labels[i]
            print('--Exec label--', label_id)
            stmts = self.blocks[label_id]
            i = self.exec_statements(stmts, i)


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def exec(self):
        return self.stmt.exec()


class Label(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        return self.value


class GoTo(Node):
    def __init__(self, label: Label, condition: ValueItem) -> None:
        self.label = label
        self.condition = condition

    def exec(self) -> Label:
        if self.condition:
            if self.condition.exec():
                return self.label
            return None
        return self.label



class Var(ValueItem):
    def __init__(self, id, value, value_type):
        super().__init__(value, value_type)
        self.id = id

    def exec(self):
        print(self.value_type + " " + self.id + " : " + str(self.value))
        return self.value


class VarAssign(TypedItem):
    def __init__(self, varL, varR):
        super().__init__(varL.value_type)
        self.varL = varL
        self.varR = varR

    def exec(self):
        self.varL.value = self.varR.exec()
        return self.varL.exec()


class Operators(TypedItem):
    def __init__(self, var, operator):
        super().__init__(var.value_type)
        self.var = var
        self.operator = operator

    def exec(self):
        if self.operator == '--':
            print('---exec op decrement---')
            self.var.value -= 1
        if self.operator == '++':
            print('---exec op increment---')
            self.var.value += 1
        return self.var.exec()


class Condition(TypedItem):
    def __init__(self, value, literal):
        super().__init__(type_bool)
        self.literal = literal
        self.value = value

    def exec(self):
        print('---exec condition ---')
        v = self.value.exec()
        l = self.literal.exec()
        return v == l


class Literal(ValueItem):
    def __init__(self, value, value_type):
        super().__init__(value, value_type)

    def exec(self):
        if self.value_type == type_int:
            return int(self.value)
        if self.value_type == type_bool:
            if self.value == 'T':
                return True
            else:
                return False
        # TODO add functions


class Empty(Node):
    def exec(self):
        pass
