from tokenrules import tokens
from ast import *

type_int = 'integer'
type_bool = 'bool'
global_var = {}


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
    '''statement : var_def
                 | '''
    p[0] = Statement(p[1])


def p_var_def(p):
    '''var_def : var LE
               | var ASSIGN literal LE
               | var ASSIGN var LE'''

    if len(p) == 3:
        p[0] = p[1]
    else:
        if p[1].value_type == p[3].value_type:
            p[1].value = p[3].value
            p[0] = p[1]
        else:
            p[0] = p[1]
            print('Syntax error', p.lineno(2))


def p_var(p):
    '''var : TYPE INT'''
    def get_from_global(id, type):
        if id not in global_var:
            global_var[id] = Var(id, None, type)
        return global_var[id]

    if p[1] == ',':
        p[0] = get_from_global(p[2], type_int)
    if p[1] == '.':
        p[0] = get_from_global(p[2], type_bool)


def p_literal_int(p):
    '''literal : INT
               | BOOL'''
    l = p[1]
    if l == 'T' or l == 'F':
        p[0] = Literal(l, type_bool)
    else:
        p[0] = Literal(l, type_int)


def p_error(p):
    print('Unexpected token:', p)
