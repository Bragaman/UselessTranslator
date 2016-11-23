import ply.lex as lex


tokens = [
    'INT'
]

reserved = {
    'T': 'BOOLVAL',
    'F': 'BOOLVAL',
    ',': 'TYPE',
    '.': 'TYPE',
    '$': 'TYPE',
    '~': 'LABEL',
    '<-': 'ASSIGN',
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

tokens += list(reserved)

t_INT = r'\d+'

