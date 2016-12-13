import ply.lex as lex
import ply.yacc as yacc
import parserrules
import tokenrules
from enviroment import *
from ast import errors_list
import ast

if __name__ == "__main__":
    lexer = lex.lex(module=tokenrules)
    parser = yacc.yacc(module=parserrules)

    code = '''
    $1 <- {
        $3
        .50 eq T please ~500
        $2
        mr eq F please ~100
            $1
            ml
        ~100
        ml eq F please ~200
            $1
            mr
        ~200
        mf eq F please ~300
            $1
            mb
        ~300
        mb eq F please ~400
            $1
            mf
        ~400
        ~500
    }
    ,30 <- -1
    .50 <- F
    $2 <- {
        ,#30
        ,10:,30 - 0  <- cur_x
        ,10:,30 - 1 <- cur_y
    }
    $3 <- {
        ,40 <- 0
        .50 <- F
         ~700
         ,10:,40 - 0
         ,10:,40 - 1
            ,10:,40 - 0 neq cur_x please ~600
            ,10:,40 - 1 neq cur_y please ~600
            .50 <- T
            .50 eq T please ~800
            ~600
            ,#40
        ,40 less ,30 please ~700
        ~800
        .50
    }
    $1
    while tp {
        $1
    }
    '''

    lab, cur = load_map('../lab.txt')
    print(cur)
    print(lab)
    if cur:
        ast.robot = Robot(cur[0], cur[1], 2, lab)
    else:
        ast.robot = Robot(0, 0, 0, lab)

    astree = parser.parse(code)
    if len(errors_list) != 0:
        for error in errors_list:
            print(error)
    else:
        print('finish build ast:')
        astree.exec()

        print(set(ast.robot.known_lab))
