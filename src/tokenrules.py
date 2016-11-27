tokens = [
    'INT', 'LE', 'ASSIGN',
    'TYPE', 'BOOL'
]

reserved = {
    '~': 'LABEL',
    ':': 'ARRAY',
    '-': 'ARRAY_OPTIONAL',
    'np': 'PASS',
    'eq': 'EQUAL',
    '#': 'OP',
    '*': 'OP',
    'mf': 'MOVEROB',
    'mb': 'MOVEROB',
    'ml': 'MOVEROB',
    'mr': 'MOVEROB',
    'tp': 'MOVEROB',
}

tokens += list(set(reserved.values()))

t_INT = r'\d+'
t_ASSIGN = r'<-'
t_TYPE = r'[\,\.\$]'
t_BOOL = r'T|F'
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