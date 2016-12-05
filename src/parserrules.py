from tokenrules import tokens
from ast import *

precedence = (
    ('right', 'ASSIGN'),
    ('nonassoc', 'COMPARE'),
)


def p_statements(p):
    '''statements : statements_list'''
    p[0] = Statements(p[1])


def p_statements_list(p):
    '''statements_list : statement statements_list
                       | '''
    if len(p) > 1:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_statement(p):
    '''statement : exp LE
                 | var_def LE
                 | go_to LE
                 | label LE
                 | while LE
                 | empty
                 '''

    p[0] = Statement(p[1])


def p_go_to(p):
    '''go_to : GO_TO label
             | exp GO_TO label'''
    if len(p) == 3:
        p[0] = GoTo(p[2], None)
    elif p[1].value_type == type_bool:
        p[0] = GoTo(p[3], p[1])
    else:
        errors_list.append("VALUE TYPE ERROR: condition should be Bool, at line: {}".format(p.lineno(2)))


def p_index(p):
    '''index : var
             | literal
             | array_var
             | '(' index ')' '''

    p[0] = p[1]


def p_indexes(p):
    '''indexes : indexes '-' index
               | '''

    if len(p) > 1:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []


def p_array(p):
    '''array_var : TYPE INT ARRAY
                  | TYPE INT ARRAY index
                  | TYPE INT ARRAY index indexes'''
    l = len(p)
    indexes = list()
    if l == 4:
        indexes.append(Literal(0, type_int))
    elif l == 5:
        indexes.append(p[4])
    elif l == 6:
        indexes.append(p[4])
        indexes += (p[5])
    if p[1] == ',':
        p[0] = Array(p[2], None, type_int, indexes)
    if p[1] == '.':
        p[0] = Array(p[2], None, type_bool, indexes)
    if p[1] == '$':
        p[0] = Array(p[2], None, type_func, indexes)


def p_var(p):
    '''var : TYPE INT
           | array_var'''

    if len(p) == 3:
        if p[1] == ',':
            p[0] = Var(p[2], None, type_int)
        if p[1] == '.':
            p[0] = Var(p[2], None, type_bool)
        if p[1] == '$':
            p[0] = Var(p[2], None, type_func)
    else:
        p[0] = p[1]


def p_label(p):
    '''label : LABEL INT'''
    p[0] = Label(p[2])


def p_literal(p):
    '''literal : INT
               | BOOL
               | '-' INT
               | PASS'''
    l = ''
    if len(p) == 3:
        l = '-' + p[2]
    else:
        l = p[1]
    if l == 'T' or l == 'F':
        p[0] = Literal(l, type_bool)
    elif l == 'np':
        p[0] = Literal(l, type_func)
    else:
        p[0] = Literal(l, type_int)


def p_var_def(p):
    '''var_def : var
               | var ASSIGN exp
               | var ASSIGN '{' statements '}'
               | var ASSIGN PASS
               '''
    l = len(p)
    if l == 2:
        p[0] = p[1]
    elif l == 4:
        if p[1].value_type == p[3].value_type:
            p[0] = VarAssign(p[1], p[3])
        else:
            p[0] = p[1]
            errors_list.append('Syntax error, at line: {}'.format(p.lineno(2)))
    else:
        p[0] = VarAssign(p[1], Function(p[4]))


def p_op(p):
    '''op : TYPE OP INT'''
    if p[1] == ',':
        var = Var(p[3], None, type_int)
        op_str = ''
        if p[2] == '#':
            op_str = '++'
        if p[2] == '*':
            op_str = '--'
        p[0] = Operators(var, op_str)


def p_binding(p):
    '''bind : var BIND var'''
    if p[3].value_type == type_func:
        p[0] = Bind(p[1], p[3], p[2])
    else:
        p[0] = p[1]
        errors_list.append("VALUE TYPE ERROR: second binding var must be func, at line: {}".format(p.lineno(2)))


def p_exp(p):
    '''exp : var
           | op
           | condition
           | literal
           | '(' exp ')'
           | bind
           '''
    l = len(p)
    if l == 2:
        p[0] = p[1]
    elif l == 4:
        p[0] = p[2]


def p_conditions(p):
    '''condition :  exp COMPARE exp'''
    if p[1].value_type != p[3].value_type:
        errors_list.append("VALUE TYPE ERROR: condition will be false, at line: {}".at(p.lineno(2)))
    p[0] = Condition(p[1], p[3], p[2])


def p_while(p):
    '''while : WHILE exp '{' statements '}' '''
    if p[2].value_type != type_bool:
        errors_list.append("VALUE TYPE ERROR: condition will be false, at line: {}".format(p.lineno(2)))
    p[0] = While(p[2], p[4])


def p_empty(p):
    '''empty : LE
             | empty LE'''
    p[0] = Empty()


def p_error(p):
    errors_list.append("Unexpected token: {}".format(p))
