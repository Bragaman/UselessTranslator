type_int = 'integer'
type_bool = 'bool'
type_label = 'label'
type_func = 'function'

global_labels = []
global_blocks = {}
global_var = {}
idToType = {}
errors_list = []


class DataNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def find_child(self, data):
        for child in self.children:
            if child.data == data:
                return child
        return None


def rec_add(indexes, i, start):
    if i < len(indexes):
        ind = indexes[i]
        i += 1
        if isinstance(ind, Array):
            if len(start.children) == 0:
                child = DataNode(Array(id, None, type, indexes))
                start.add_child(child)
                # print(child.data.id, ';')
                return child.data
            return start.children[0].data
        else:
            index = ind.exec()
            # print(index, '->')
            child = start.find_child(index)
            if not child:
                child = DataNode(index)
                start.add_child(child)
            return rec_add(indexes, i, child)


def get_from_global_array(id, type, indexes):
    check_type = idToType.get(id, None)
    if check_type == type:
        root = global_var[id]
        # print('start array')
        indexes.append(Array(id, None, type, indexes))
        return rec_add(indexes, 0, root)

    elif not check_type:
        idToType[id] = type
        root = DataNode(id)
        indexes.append(Array(id, None, type, indexes))
        result = rec_add(indexes, 0, root)

        global_var[id] = root
        return result
    else:
        errors_list.append("VALUE TYPE ERROR: in variable with ID {}".format(id))
        return Array(id, None, type, indexes)


def get_from_global(id, type, indexes=list()):
    if len(indexes) == 0:
        check_type = idToType.get(id, None)
        if check_type == type:
            pass
        elif not check_type:
            idToType[id] = type
            global_var[id] = Var(id, None, type)
        else:
            errors_list.append("VALUE TYPE ERROR: in variable with ID {}".format(id))
        return global_var.get(id)
    else:
        return get_from_global_array(id, type, indexes)


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


class AbstaractVar(ValueItem):
    def __init__(self, id, value, value_type):
        super().__init__(value, value_type)
        self.id = id
        self.binding_funcs = []
        self.is_in_func = False

    def init_from_global(self):
        raise NotImplementedError

    def sync_with_global(self):
        raise NotImplementedError

    def exec(self):
        self.init_from_global()
        if not self.is_in_func and len(self.binding_funcs) > 0:
            print('----Start exec BINDING FUNC-----')
            self.is_in_func = True
            for binding_func in self.binding_funcs:
                binding_func.exec()
            self.is_in_func = False
            print('----Finish exec BINDING FUNC-----')
        if self.value_type == type_func:
            if self.value:
                return self.value.exec()
        else:
            print(self.value_type + " " + self.id + " : " + str(self.value))
            return self.value


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
    def __init__(self, stmts: Statements) -> None:
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


class Var(AbstaractVar):
    # def __init__(self, id, value, value_type):
    #     super().__init__(value, value_type)
    #     self.id = id
    #     self.binding_funcs = []
    #     self.is_in_func = False

    def init_from_global(self):
        tmp = get_from_global(self.id, self.value_type)
        self.value = tmp.value
        self.binding_funcs = tmp.binding_funcs

    def sync_with_global(self):
        tmp = get_from_global(self.id, self.value_type)
        tmp.value = self.value
        tmp.binding_funcs = self.binding_funcs

        # def exec(self):
        #     self.init_from_global()
        #     if not self.is_in_func and len(self.binding_funcs) > 0:
        #         print('----Start exec BINDING FUNC-----')
        #         self.is_in_func = True
        #         for binding_func in self.binding_funcs:
        #             binding_func.exec()
        #         self.is_in_func = False
        #         print('----Finish exec BINDING FUNC-----')
        #     if self.value_type == type_func:
        #         if self.value:
        #             return self.value.exec()
        #     else:
        #         print(self.value_type + " " + self.id + " : " + str(self.value))
        #         return self.value


class Array(AbstaractVar):
    def __init__(self, id, value, value_type, indexes):
        super().__init__(id, value, value_type)
        self.indexes = indexes

    def init_from_global(self):
        l = []
        for i in self.indexes:
            l.append(i)
            # l.append(i.exec())
        tmp = get_from_global(self.id, self.value_type, l)
        self.value = tmp.value
        self.binding_funcs = tmp.binding_funcs
        self.indexes = tmp.indexes

    def sync_with_global(self):
        l = []
        for i in self.indexes:
            # l.append(i.exec())
            l.append(i)
        tmp = get_from_global(self.id, self.value_type, l)
        tmp.value = self.value
        tmp.binding_funcs = self.binding_funcs
        tmp.indexes = self.indexes


class VarAssign(TypedItem):
    def __init__(self, var_l: AbstaractVar, var_r: Node) -> None:
        super().__init__(var_l.value_type)
        self.varL = var_l
        self.varR = var_r

    def exec(self):
        result = None
        self.varL.init_from_global()
        if self.value_type == type_func:
            if isinstance(self.varR, Var):
                self.varR.init_from_global()
                self.varL.value = self.varR.value
            elif isinstance(self.varR, Function):
                self.varL.value = self.varR.stmts
            self.varL.sync_with_global()
        else:
            self.varL.value = self.varR.exec()
            self.varL.sync_with_global()
            result = self.varL.exec()
        return result


class Operators(TypedItem):
    def __init__(self, var, operator):
        super().__init__(var.value_type)
        self.var = var
        self.operator = operator

    def exec(self):
        self.var.init_from_global()
        if self.operator == '--':
            print('---exec op decrement---')
            self.var.value -= 1
        if self.operator == '++':
            print('---exec op increment---')
            self.var.value += 1
        self.var.sync_with_global()
        return self.var.exec()


class Bind(Node):
    def __init__(self, var: AbstaractVar, var_func: AbstaractVar, action: str) -> None:
        self.var = var
        self.var_func = var_func
        self.action = action

    def exec(self) -> bool:
        self.var.init_from_global()
        self.var_func.init_from_global()
        result = True
        if self.action == '@':
            self.var.binding_funcs.append(self.var_func)
            # TODO add check

        if self.action == '%':
            try:
                self.var.binding_funcs.remove(self.var_func)
            except ValueError:
                pass

        self.var.sync_with_global()
        return result


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
