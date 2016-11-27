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


class Literal(Node):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type

    def exec(self):
        print(self.value)
        return self.value
