from tokenrules import tokens
from ast import *

type_int = 'integer'
type_bool = 'bool'
type_label = 'label'


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
    '''statement : int_exp LE
                 | var_def LE
                 | go_to LE
                 | label LE
                 | empty
                 '''
    p[0] = Statement(p[1])


def p_go_to(p):
    '''go_to : GO_TO label'''
    p[0] = GoTo(p[2])


def p_var_def(p):
    '''var_def : var
               | var ASSIGN literal
               | var ASSIGN var'''

    if len(p) == 3:
        p[0] = p[1]
    else:
        if p[1].value_type == p[3].value_type:
            p[0] = VarAssign(p[1], p[3])
        else:
            p[0] = p[1]
            print('Syntax error', p.lineno(2))


def p_var(p):
    '''var : TYPE INT'''

    if p[1] == ',':
        p[0] = get_from_global(p[2], type_int)
    if p[1] == '.':
        p[0] = get_from_global(p[2], type_bool)


def p_label(p):
    '''label : LABEL INT'''
    p[0] = Label(p[2])


def p_literal(p):
    '''literal : INT
               | BOOL'''
    l = p[1]
    if l == 'T' or l == 'F':
        p[0] = Literal(l, type_bool)
    else:
        p[0] = Literal(l, type_int)


def p_int_op(p):
    '''int_exp : TYPE OP INT'''

    if p[1] == ',':
        var = get_from_global(p[3], type_int)
        op_str  = ''
        if p[2] == '#':
            op_str = '++'
        if p[2] == '*':
            op_str = '--'
        p[0] = IntExpr(var, op_str)


def p_empty(p):
    '''empty : LE
             | empty LE'''
    p[0] = Empty()

def p_error(p):
    print('Unexpected token:', p)
