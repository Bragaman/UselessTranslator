tokens = [
    'INT', 'LE', 'ASSIGN',
    'TYPE', 'BOOL', 'LABEL',
    'OP', 'GO_TO', 'WHILE',
    'PASS', 'COMPARE',
    'BIND', 'ARRAY', 'ROBOT'
]

reserved_map = {
    # 'mf': 'MOVEROB',
    # 'mb': 'MOVEROB',
    # 'ml': 'MOVEROB',
    # 'mr': 'MOVEROB',
    # 'tp': 'MOVEROB',
}

literals = "{}()-"
tokens += list(set(reserved_map.values()))

t_INT = r'\d+'
t_ASSIGN = r'<-'
t_TYPE = r'[\,\.\$]'
t_BOOL = r'T|F'
t_LABEL = r'\~'
t_OP = r'\#|\*'
t_GO_TO = r'please'
t_WHILE = r'while'
t_PASS = r'np'
t_COMPARE = r'eq|neq'
t_BIND = r'@|%'
t_ARRAY = r'\:'
t_ROBOT = r'mf|mb|ml|mr|tp|cur_x|cur_y'
# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    t.type = "LE"
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)