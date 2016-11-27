import ply.lex as lex
import ply.yacc as yacc
import parserrules
import tokenrules


if __name__ == "__main__":
    lexer = lex.lex(module=tokenrules)
    parser = yacc.yacc(module=parserrules)

    code = ''',1 <- 10
    .2 <- T
    '''
    # lexer.input(code)

    # while True:
    #     tok = lexer.token()  # читаем следующий токен
    #     if not tok:
    #         break  # закончились печеньки
    #     print(tok)
    #
    parser.parse(code).exec()