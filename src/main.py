import ply.lex as lex
import ply.yacc as yacc
import parserrules
import tokenrules


if __name__ == "__main__":
    lexer = lex.lex(module=tokenrules)
    parser = yacc.yacc(module=parserrules)

    code = '''
    ,2 <- 10
    $1 <- {
        ,*2
    }
    while (,2 eq 5) eq F {
        $1
    }
    '''

    ast = parser.parse(code)
    print('finish build ast:')
    ast.exec()
