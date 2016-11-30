from tokenrules import tokens
from ast import *

global_var = {}


def get_from_global(id, type):
    if id not in global_var:
        global_var[id] = Var(id, None, type)
    return global_var[id]


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
    '''statement : op LE
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
        print('VALUE TYPE ERROR: condition should be Bool, at line:', p.lineno(2))


def p_var(p):
    '''var : TYPE INT'''

    if p[1] == ',':
        p[0] = get_from_global(p[2], type_int)
    if p[1] == '.':
        p[0] = get_from_global(p[2], type_bool)
    if p[1] == '$':
        p[0] = get_from_global(p[2], type_func)


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
        l = '-'+p[2]
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
            print('Syntax error', p.lineno(2))
    else:
        p[0] = VarAssign(p[1], Function(p[4]))



def p_op(p):
    '''op : TYPE OP INT'''

    if p[1] == ',':
        var = get_from_global(p[3], type_int)
        op_str = ''
        if p[2] == '#':
            op_str = '++'
        if p[2] == '*':
            op_str = '--'
        p[0] = Operators(var, op_str)


def p_exp(p):
    '''exp : var
           | op
           | condition
           | literal
           | '(' exp ')'
           '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_conditions(p):
    '''condition :  exp EQ exp'''
    if p[1].value_type != p[3].value_type:
        print('VALUE TYPE ERROR: condition will be false, at line:', p.lineno(2))
    p[0] = Condition(p[1], p[3])


def p_while(p):
    '''while : WHILE exp '{' statements '}' '''
    if p[2].value_type != type_bool:
        print('VALUE TYPE ERROR: condition will be false, at line:', p.lineno(2))
    p[0] = While(p[2], p[4])


def p_empty(p):
    '''empty : LE
             | empty LE'''
    p[0] = Empty()


def p_error(p):
    print('Unexpected token:', p)
