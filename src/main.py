import ply.lex as lex
import ply.yacc as yacc
import parserrules
import tokenrules


if __name__ == "__main__":
    lexer = lex.lex(module=tokenrules)
    parser = yacc.yacc(module=parserrules)

    code = '''
    ,1 <- ,2 <- 15
    ,3 <- ,#2
    '''

    ast = parser.parse(code)
    print('finish build ast:')
    ast.exec()