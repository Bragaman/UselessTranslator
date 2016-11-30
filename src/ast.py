type_int = 'integer'
type_bool = 'bool'
type_label = 'label'
type_func = 'function'

global_labels = []
global_blocks = {}
errors_list = []


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


class While(Node):
    def __init__(self, condition: ValueItem, stmts: Statements) -> None:
        self.condition = condition
        self.stmts = stmts

    def exec(self):
        print('----Start exec while-----')
        while self.condition.exec():
            self.stmts.exec()
        print('----Finish exec while-----')


class Function(Node):
    def __init__(self, stmts: Statements) ->None:
        self.stmts = stmts

    def exec(self):
        print('----Start exec func-----')
        if self.stmts:
            self.stmts.exec()
        print('----Finish exec while-----')


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
        self.binding_funcs = []
        self.is_in_func = False

    def exec(self):
        if not self.is_in_func and len(self.binding_funcs) > 0:
            print('----Start exec BINDING FUNC-----')
            self.is_in_func = True
            for binding_func in self.binding_funcs:
                binding_func.exec()
            self.is_in_func = False
            print('----Finish exec BINDING FUNC-----')
        if self.value_type == type_func:
            return self.value.exec()
        else:
            print(self.value_type + " " + self.id + " : " + str(self.value))
            return self.value


class VarAssign(TypedItem):
    def __init__(self, varL, varR):
        super().__init__(varL.value_type)
        self.varL = varL
        self.varR = varR

    def exec(self):
        if self.value_type == type_func:
            self.varL.value = self.varR.stmts
            return None
        else:
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


class Bind(Node):
    def __init__(self, var: Var, var_func: Var, action: str) -> None:
        self.var = var
        self.var_func = var_func
        self.action = action

    def exec(self) -> bool:
        if self.action == '@':
            self.var.binding_funcs.append(self.var_func)
            # TODO add check
            return True
        if self.action == '%':
            self.var.binding_funcs.remove(self.var_func)
            return True
        return False


class Condition(TypedItem):
    operators = {
        'eq': lambda r, l: r == l,
        'neq': lambda r, l: r != l,
    }

    def __init__(self, varL, varR, operator):
        super().__init__(type_bool)
        self.varR = varR
        self.varL = varL
        self.operator = operator

    def exec(self):
        print('---exec condition ---')
        r = self.varR.exec()
        l = self.varL.exec()
        return Condition.operators[self.operator](r, l)


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
        if self.value_type == type_func:
            return None


class Empty(Node):
    def exec(self):
        pass
