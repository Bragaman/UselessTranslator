import ply.lex as lex
import ply.yacc as yacc
import parserrules
import tokenrules
from ast import errors_list


if __name__ == "__main__":
    lexer = lex.lex(module=tokenrules)
    parser = yacc.yacc(module=parserrules)

    code = '''
    ,1 <- 1
    ,5:1-,1 <- 1
    ,#1
    ,5:1-,1 <- 2
    ,#1
    ,5:1-,1 <- 3
    ,6 <- ,5:1-1
    ,7 <- ,5:1-2
    ,8 <- ,5:1-3
    '''

    ast = parser.parse(code)
    if len(errors_list) != 0:
        for error in errors_list:
            print(error)
    else:
        print('finish build ast:')
        ast.exec()
