#!/usr/bin/python
import ply.yacc as yacc
import logging
import sys, re
from collections import defaultdict
from pprint import pprint
#get tokens
#import lexer #as ourLexer# our lexer
# tokens = lexer.tok_data
import lexer
tokens = lexer.tokens

identifier = {}
identifierList = []

def p_start(p):
#ignored extra
#module = stmt ^* (';' / IND{=})
    '''start : stmtIndentSemicolon ENDMARKER
            | stmt ENDMARKER'''
    p[0] = p[1]

def p_stmtIndentSemicolon(p):
    '''stmtIndentSemicolon : stmt NEWLINE stmtIndentSemicolon
                            | stmt SEMICOLON stmtIndentSemicolon
                            | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    '''stmt : complexOrSimpleStmt '''
    p[0] = p[1]

def p_stmtStar(p):                      # changed a bit
    '''stmtStar : stmt NEWLINE stmtStar
                 | stmt SEMICOLON stmtStar
                 | stmt'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_suite(p):                         # changed it too
    '''suite : simpleStmt
                  | NEWLINE INDGR stmtStar INDLE'''
    if len(p) > 2:
        p[0] = p[3]
    else:
        p[0] = [p[1]]

def p_typeDefSuite(p):                         # changed it too
    '''typeDefSuite : typeDef
              | NEWLINE INDGR typeDefStar INDLE'''
    if len(p) > 2:
        p[0] = p[3]
    else:
        p[0] = [p[1]]

def p_typeDefStar(p):                      # changed a bit
    '''typeDefStar : typeDef NEWLINE typeDefStar
                 | typeDef SEMICOLON typeDefStar
                 | typeDef'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_constantSuite(p):                         # changed it too
    '''constantSuite : constant
              | NEWLINE INDGR constantStar INDLE'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_constantStar(p):                      # changed a bit
    '''constantStar : constant NEWLINE constantStar
                 | constant SEMICOLON constantStar
                 | constant'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_variableSuite(p):                         # changed it too
    '''variableSuite : variable
              | NEWLINE INDGR variableStar INDLE'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_variableStar(p):                      # changed a bit
    '''variableStar : variable NEWLINE variableStar
                 | variable SEMICOLON variableStar
                 | variable'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_complexOrSimpleStmt(p):
    '''complexOrSimpleStmt : ifStmt
                            | whenStmt
                            | whileStmt
                            | forStmt
                            | caseStmt
                            | tryStmt
                            | simpleStmt
                            | blockStmt
                            | staticStmt
                            | deferStmt
                            | asmStmt
                            | PROC routine
                            | MACRO routine
                            | ITERATOR routine
                            | METHOD routine
                            | TYPE typeDefSuite
                            | CONST constantSuite
                            | LET variableSuite
                            | VAR variableSuite '''
    if len(p) > 2:
        p[0] = {'type': p[1], 'content': p[2]}
    else:
        p[0] = p[1]
                            ## bind and mixin are also not implemented
                            ## we are not implementing 'template' routine , 'converter'

def p_simpleStmt(p):
    '''simpleStmt : returnStmt
                | raiseStmt
                | yieldStmt
                | discardStmt
                | breakStmt
                | continueStmt
                | pragmaStmt
                | importStmt
                | echoStmt
                | fromStmt
                | includeStmt
                | exprStmt
                | incStmt'''
    p[0] = p[1]

## we are not implementing exportStmt

def p_exprStmt(p):
    #not doing lhs expr exprStmtInter2 doBlocks
    # '''exprStmt : simpleExpr
    #             | lhs exprStmtInter
    #             | IDENTIFIER exprStmtInter'''
    # '''exprStmt : simpleExpr
    #             | lhs EQUALS expr
    #             | IDENTIFIER EQUALS expr'''
    '''exprStmt : simpleExpr exprStmtInter'''

    print "exprStmt has %d len"%(len(p))
    if len(p)==2:
        p[0]=p[1]
    return
    p[0] = {
	      'place' : 'undef',
	      'type' : 'ERROR_TYPE'
    }
    if p[3]['type'] == 'ERROR_TYPE':
        return
    #identifier will have attri. name, type and place
    lhsIdentifier=p[1]['name']
    lhsType=p[1]['type']
    lhsPlace=p[1]['place']
    if lhsType!=p[3]['type']:
        msg_error('Type mismatch in assignment with variable (%s)!'%lhsIdentifier)
    else:
        print "=, %s, %s" %(p[1]['place'],p[3]['place'])


def p_exprStmtInter(p):
    ''' exprStmtInter : EQUALS expr
                      | expr exprStmtInter2 doBlocks
                      | empty'''


def p_exprStmtInter2(p):
    ''' exprStmtInter2 : COMMA expr exprStmtInter2
                       | empty '''

def p_whileStmt(p):
    '''whileStmt : WHILE condStmt'''
    p[0] = {
    'inline': False,
    'type': p[1],
    'cond': p[2]['cond'],
    'then': p[2]['then']
    }

def p_identWithPragmaInter(p):
    '''identWithPragmaInter : COMMA identWithPragma identWithPragmaInter
                            | empty'''

def p_identWithPragma(p):
    '''identWithPragma : identVis pragmaInter'''

def p_pragmaInter(p):
    '''pragmaInter : pragma
                    | empty'''

def p_pragma(p):
    '''pragma : CURLYDOTLE pragmaInterInter optPar CURLYDOTRI
               | CURLYDOTLE pragmaInterInter optPar CURLYRI'''

def p_pragmaInterInter(p):
    '''pragmaInterInter : expr COLON expr pragmaInter
                   | empty'''

def p_pragmaStmt(p):
    '''pragmaStmt : pragma pragmaStmtInter'''

def p_pragmaStmtInter(p) :
    ''' pragmaStmtInter : COLON suite
                        | empty '''

def p_optpar(p):
    '''optPar : NEWLINE
              | NEWLINE INDGR
              | empty'''

def p_identVis(p):
    '''identVis : symbol '''  # oprInter''' should be opr = `+*` sort of
    p[0] = p[1]

def p_oprInter(p):
    #should be opr
    '''oprInter : empty'''

def p_forStmt(p):
    '''forStmt : FOR identWithPragma identWithPragmaInter IN expr COLON suite'''

def p_tryStmt(p):
    '''tryStmt : TRY COLON suite exceptInter finallyInter'''
    p[0] = {
    'type': p[1],
    'try': p[3],
    'except': p[4],
    'finally': p[5]
    }

def p_exceptInter(p):
    '''exceptInter : EXCEPT expr COLON suite exceptInter
                   | empty'''
    if len(p) > 2:
        p[0] = [{'except': p[2], 'then': p[4]}] + p[5]
    else:
        p[0] = [p[1]]

def p_finallyInter(p):
    '''finallyInter : FINALLY COLON suite
                    | empty'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_ifStmt(p):
    '''ifStmt : IF condStmt elifStmt elseStmt'''
    p[0] = {
    'inline': False,
    'type': p[1],
    'cond': p[2]['cond'],
    'then': p[2]['then'],
    'elif': p[3],
    'else': p[4]
    }

def p_whenStmt(p):
    '''whenStmt : WHEN condStmt elifStmt elseStmt'''
    p[0] = {
    'inline': False,
    'type': p[1],
    'cond': p[2]['cond'],
    'then': p[2]['then'],
    'elif': p[3],
    'else': p[4]
    }

def p_condStmt(p):
    '''condStmt : expr COLON suite'''
    p[0] = {
    'inline': False,
    'cond': p[1],
    'then': p[2]
    }

def p_elseStmt(p):
    '''elseStmt : ELSE COLON suite
                    | empty'''
    if len(p) > 2:
        p[0] = {
        'inline': False,
        'type': p[1],
        'then': p[3]
        }
    else:
        p[0] = p[1]

def p_elifStmt(p):
    '''elifStmt : ELIF condStmt elifStmt
                    | empty'''
    if len(p) > 2:
        p[0] = {
        'inline': False,
        'type': p[1],
        'cond': p[2]['cond'],
        'then': p[2]['then'],
        'next': p[3]
        }
    else:
        p[0] = p[1]

def p_exprList(p):
    '''exprList : expr COMMA exprList
                | expr'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_ofBranch(p):
    '''ofBranch : OF exprList COLON suite'''
    p[0] = {
    'cond': p[2],
    'then': p[4]
    }

def p_ofBranches(p):
    '''ofBranches : ofBranch ofBranches
                    | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_caseStmt(p):
    '''caseStmt : CASE expr COLON NEWLINE INDGR ofBranch ofBranches elifStmt elseStmt INDLE'''
    p[0] = {
    'inline': False,
    'type': p[1],
    'case': p[2],
    'branches': [p[6]] + p[7],
    'elif': p[8],
    'else': p[9]
    }

def p_echoStmt(p):
    '''echoStmt : ECHO exprList'''
    p[0] = {
    'type': p[1],
    'echo': p[2]
    }

def p_importStmt(p):
    '''importStmt : IMPORT exprList
                | IMPORT expr EXCEPT exprList'''
    if len(p) > 3:
        p[0] = {
        'type': p[1],
        'import': p[2],
        'except': None
        }
    else:
        p[0] = {
        'type': p[1],
        'import': p[2],
        'except': p[4]
        }

def p_includeStmt(p):
    '''includeStmt : INCLUDE exprList''' # should be list of IDENTIFIER instead of exprList
    p[0] = {
    'type': p[1],
    'include': p[2]
    }

def p_fromStmt(p):
    '''fromStmt : FROM IDENTIFIER IMPORT exprList'''
    p[0] = {
    'type': p[1],
    'from': p[2],
    'import': p[4]
    }

def p_returnStmt(p):
    '''returnStmt : RETURN expr
                | RETURN'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'return': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'return': None
        }

def p_raiseStmt(p):
    '''raiseStmt : RAISE expr
                | RAISE'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'raise': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'raise': None
        }

def p_yieldStmt(p):
    '''yieldStmt : YIELD expr
                | YIELD'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'yield': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'yield': None
        }

def p_discardStmt(p):
    '''discardStmt : DISCARD expr
                | DISCARD'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'discard': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'discard': None
        }

def p_breakStmt(p):
    '''breakStmt : BREAK expr
                | BREAK'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'break': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'break': None
        }

def p_continueStmt(p):
    '''continueStmt : CONTINUE expr
                | CONTINUE'''
    if len(p) > 2:
        p[0] = {
        'type': p[1],
        'continue': p[2]
        }
    else:
        p[0] = {
        'type': p[1],
        'continue': None
        }

def p_incStmt(p):
    '''incStmt : INC expr'''
    p[0] = {
    'type': p[1],
    'increment': p[2]
    }

def p_blockStmt(p):
    '''blockStmt : BLOCK symbol COLON suite
                | BLOCK COLON suite'''
    if len(p) > 4:
        p[0] = {
        'type': p[1],
        'symbol': p[2],
        'block': p[4]
        }
    else:
        p[0] = {
        'type': p[1],
        'symbol': None,
        'block': p[3]
        }

def p_staticStmt(p):
    '''staticStmt : STATIC COLON suite'''
    p[0] = {
    'type': p[1],
    'static': p[2]
    }

def p_deferStmt(p):
    '''deferStmt : DEFER COLON suite'''
    p[0] = {
    'type': p[1],
    'defer': p[2]
    }

def p_asmStmt(p):
    '''asmStmt : ASM pragma strings
                | ASM strings'''

def p_strings(p):
    '''strings : STRLIT
                | RSTRLIT
                | TRIPLESTRLIT'''
    p[0] = p[1]

def p_expr(p):
    '''expr : ifExpr
            | whenExpr
            | caseExpr
            | simpleExpr'''
    p[0] = p[1]

def p_ifExpr(p):
    '''ifExpr : IF condExpr elifExpr elseExpr'''
    p[0] = {
    'inline': True,
    'type': p[1],
    'cond': p[2]['cond'],
    'then': p[2]['then'],
    'elif': p[3],
    'else': p[4]
    }

def p_whenExpr(p):
    '''whenExpr : WHEN condExpr elifExpr elseExpr'''
    p[0] = {
    'inline': True,
    'type': p[1],
    'cond': p[2]['cond'],
    'then': p[2]['then'],
    'elif': p[3],
    'else': p[4]
    }

def p_condExpr(p):
    '''condExpr : expr COLON expr'''
    p[0] = {
    'inline': True,
    'cond': p[1],
    'then': p[3],
    }

def p_elifExpr(p):
    '''elifExpr : ELIF expr COLON expr elifExpr
        | empty'''
    if len(p) > 2:
        p[0] = {
        'inline': True,
        'type': p[1],
        'cond': p[2],
        'then': p[4],
        'next': p[5],
        }
    else:
        p[0] = p[1]

def p_elseExpr(p):
    '''elseExpr : ELSE COLON expr
        | empty'''
    if len(p) > 2:
        p[0] = {
        'inline': True,
        'type': p[1],
        'then': p[3],
        }
    else:
        p[0] = p[1]

def p_caseExpr(p):
    '''caseExpr : CASE expr COLON NEWLINE INDGR ofBranch ofBranches elifExpr elseExpr INDLE'''
    p[0] = {
    'inline': True,
    'type': p[1],
    'case': p[2],
    'branches': [p[6]] + p[7],
    'elif': p[8],
    'else': p[9]
    }

def p_simpleExpr(p):
    '''simpleExpr : arrowExpr interOne'''
    # p[0] = {
    # 'type' : 'simple'
    # }
    if p[2]['type']==None:
        p[0]=p[1]

def p_interOne(p):
    '''interOne : OP0 arrowExpr interOne
                | empty '''
    p[0] = {
    'type:' ("OP0" if len(p) > 2 else None),
    'value': p[1],
    }
    if len(p) > 2:
        msg_error(p,"Arrow like Operators not supported")

def p_arrowExpr(p):
    '''arrowExpr : assignExpr
                | assignExpr OP1 assignExpr'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = {
        'place': 'undef',
        'type': 'ERROR_TYPE'
        }
        if p[1]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
            msg_error(p,'Unsupported type')
        elif p[1]['type']!=p[3]['type']:
            msg_error(p,'Type mismatch')
        else:
            TAC.emit(p[2][0],p[1]['place'],p[1]['place'],p[3]['place'])
            p[0] = p[1]
        # p[0] = {
        # 'type:' ("OP1" if len(p) > 2 else None),
        # 'value': p[1],
        # 'place'
        # }

# def p_interTwo(p):
#     '''interTwo : OP1 assignExpr interTwo
#                 | empty '''

def p_assignExpr(p):
    '''assignExpr : orExpr interThree'''
    if p[2]['type']==None:
        p[0]=p[1]

def p_interThree(p):
    '''interThree : OP2 orExpr interThree
                | empty '''
    p[0] = {
    'type:' ("OP2" if len(p) > 2 else None),
    'value': p[1],
    }
    if len(p) > 2:
        msg_error(p,p[1]+" operators not supported")

def p_orExpr(p): # Assuming Bitwise integer operations
    '''orExpr : andExpr interFour'''
    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }

def p_interFour(p):
    '''interFour : OR andExpr interFour
                | XOR andExpr interFour
                | empty '''
    if len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }


def p_andExpr(p):
    '''andExpr : cmpExpr interFive'''
    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }

def p_interFive(p):
    '''interFive : AND cmpExpr interFive
                | empty '''
    if len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }

def p_cmpExpr(p):
    '''cmpExpr : sliceExpr interSix'''
    if p[2]['place']==None:
        p[0]=p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    elif:
        p[1]['type']=='BOOLEAN':
        msg_error(p,"Boolean not allowed in comparision statements")
    else:
        temp = TAC.createTemp()
        label1 = TAC.newLabel()
        label2 = TAC.newLabel()
        TAC.emit('ifgoto',p[2]['value'],p[1]['place'],p[2]['place'],label1['name'])
        TAC.emit('=', temp, 0)
        TAC.emit("goto", label2['name'])
        TAC.emit("label", label1['name'])
        TAC.emit('=' temp, 1)
        TAC.emit("label", label2['name'])
        p[0] = {
        'type': 'BOOLEAN',
        'place': temp
        }


def p_interSix(p):
    '''interSix : OP5 sliceExpr interSix
                | empty '''

    if len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit('ifgoto',p[3]['value'],p[2]['place'],p[3]['place'],label1['name'])
        TAC.emit('=', temp, 0)
        TAC.emit("goto", label2['name'])
        TAC.emit("label", label1['name'])
        TAC.emit('=' temp, 1)
        TAC.emit("label", label2['name'])
        p[0] = {
        'type': 'BOOLEAN',
        'value': p[1],
        'place': temp
        }

def p_sliceExpr(p):           # ignored right now just like arrow
    '''sliceExpr : ampExpr interSeven'''

    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }



def p_interSeven(p):
    '''interSeven : DOTDOT ampExpr interSeven
                | empty '''

    if len(p)>2:
        msg_error(p,'DOT DOT not implemented right now')
    elif len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }

def p_ampExpr(p):                           # ignored right now just like arrow
    '''ampExpr : plusExpr interEight'''

    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }



def p_interEight(p):
    '''interEight : OP7 plusExpr interEight
                | empty '''

    if len(p)>2:
        msg_error(p,'& not implemented right now')
    elif len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }
def p_plusExpr(p):
    '''plusExpr : mulExpr interNine'''

    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }


def p_interNine(p):
    '''interNine : OP8 mulExpr interNine
                | empty '''

    if len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }

def p_mulExpr(p):
    '''mulExpr : dollarExpr interTen'''

    if p[2]['place']==None:
        p[0] = p[1]
    elif p[1]['type']=='ERROR_TYPE' or p[2]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[1]['type']!=p[2]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[2]['value'],temp,p[1]['place'],p[2]['place'])
        p[0] = {
        'type': p[1]['type'],
        'place': temp
        }

def p_interTen(p):
    '''interTen : OP9 dollarExpr interTen
                | empty '''

    if len(p)==2:
        p[0] = {
        'type': None,
        'value': None,
        'place': None
        }
    elif p[2]['type']=='ERROR_TYPE' or p[3]['type']=='ERROR_TYPE':
        msg_error(p,'Unsupported type')
    elif p[3]['place']==None:
        p[0] = {
        'type': p[2]['type']
        'value': p[1],
        'place': p[2]['place']
        }
    elif p[2]['type']!=p[3]['type']:
        msg_error(p,'Type mismatch')
    else:
        temp = TAC.createTemp()
        TAC.emit(p[3]['value'],temp,p[2]['place'],p[3]['place'])
        p[0] = {
        'type': p[2]['type'],
        'value': p[1],
        'place': temp
        }

        
def p_dollarExpr(p):
    '''dollarExpr : primary interElev'''

def p_interElev(p):
    '''interElev : OP10 primary interElev
                | empty '''

def p_castExpr(p):
    '''castExpr : CAST BRACKETLE simpleExpr BRACKETRI PARLE expr PARRI'''

def p_primary(p):
    '''primary : typeKeyw typeDescK
                | interPrefixOperator identOrLiteral interPrimarySuffix
                | STATIC primary
                | BIND primary'''
#shd be interPrefixOperator identOrLiteral interPrimarySuffix

def p_interPrefixOperator(p):
    '''interPrefixOperator : prefixOperator interPrefixOperator
                            | empty '''

def p_interPrimarySuffix(p):
    '''interPrimarySuffix : primarySuffix interPrimarySuffix
                            | empty '''

def p_identOrLiteral(p):
    # '''identOrLiteral : symbol
    #                   | literal
    #                   | par
    #                   | IDENTIFIER'''
    '''identOrLiteral :  literal
                        | castExpr
                        | arrayConstr
                        | tupleConstr
                        | symbol '''
    # '''identOrLiteral :  literal
    #                     | castExpr
    #                     | symbol
    #                     | lhs'''
    p[0] = p[1]

def p_lhs(p):
    '''lhs : arrayConstr
            | tupleConstr'''
    p[0] = p[1]

def p_arrayConstr(p):
    ''' arrayConstr : BRACKETLE arrayConstrInter BRACKETRI '''

def p_arrayConstrInter(p) :
    ''' arrayConstrInter : exprColonEqExpr COMMA arrayConstrInter
                         | exprColonEqExpr  arrayConstrInter
                         | empty'''


def p_tupleConstr(p):
    ''' tupleConstr : PARLE tupleConstrInter PARRI '''

def p_tupleConstrInter(p) :
    ''' tupleConstrInter : exprColonEqExpr COMMA tupleConstrInter
                         | exprColonEqExpr  tupleConstrInter
                         | empty'''


def p_exprColonEqExpr(p) :
    ''' exprColonEqExpr : expr
                        | expr COLON expr
                        | expr EQUALS expr '''


def p_typeKeyw(p):
    '''typeKeyw : VAR
                | OUT
                | PTR
                | REF
                | SHARED
                | TUPLE
                | ARRAY
                | PROC
                | ITERATOR
                | DISTINCT
                | OBJECT
                | ENUM
                | INT
                | INT8
                | INT16
                | INT32
                | INT64
                | FLOAT
                | FLOAT8
                | FLOAT16
                | FLOAT32
                | FLOAT64
                | CHAR
                | STRING '''
    p[0] = p[1]

def p_typeDescK(p):
    '''typeDescK : simpleExpr
                 | empty'''
    p[0] = p[1]

def p_primarySuffix(p):
    '''primarySuffix : doBlocks
                     | PARLE primarySuffixInter PARRI
                     | DOT symbol
                     | BRACKETLE exprList BRACKETRI
                     | CURLYLE exprList CURLYRI'''

## we are not implementing generalised lit etc  ## Last rule is also not implemented

def p_primarySuffixInter(p):
    ''' primarySuffixInter : exprColonEqExpr COMMA primarySuffixInter
                           | exprColonEqExpr  primarySuffixInter
                           | empty'''

def p_prefixOperator(p):
    '''prefixOperator : operator'''

def p_symbol(p):
    '''symbol : IDENTIFIER
                | ADDR
                | TYPE
                | BOOLEAN'''
    p[0] = p[1]

def p_literal(p):
    '''literal : INTLIT
                | INT8LIT
                | INT16LIT
                | INT32LIT
                | INT64LIT
                | FLOATLIT
                | FLOAT32LIT
                | FLOAT64LIT
                | CHARLIT
                | strings
                | NIL'''
    p[0] = p[1]
# def p_par(p):

def p_doBlocks(p):
    '''doBlocks : doBlock NEWLINE doBlocks
                | empty '''
    if len(p) > 2:
        p[0] = {
        'type': 'do',
        'blocks': [p[1]] + p[3]
        }
    else:
        p[0] = {
        'type': 'do',
        'blocks': [p[1]]
        }

def p_doBlock(p):
    '''doBlock : DO COLON suite'''
    p[0] = p[3]

def p_operator(p):
    '''operator : OP0
                | OP1
                | OP2
                | OP5
                | OP6
                | OP7
                | OP8
                | OP9
                | OR
                | AND
                | XOR
                | IS
                | ISNOT
                | NOTIN
                | IN
                | OF
                | DIV
                | MOD
                | SHL
                | SHR
                | NOT
                | STATIC
                | DOTDOT'''
    p[0] = p[1]

def p_routine(p):
    ''' routine : identVis paramListColon EQUALS suite '''

def p_typeKeyww(p):
    ''' typeKeyww : INT
                    | FLOAT
                    | CHAR
                    | STRING '''
    p[0] = p[1]

def p_paramListColon(p):
    ''' paramListColon : paramListInter
                        | paramListInter COLON typeDescK'''
    p[0] = {
    'vars': p[1],
    'type': (p[3] if len(p)>2 else None)
    }

def p_paramListInter(p):
    ''' paramListInter : PARLE declColonEqualsInter2 PARRI'''
    p[0] = p[2]

def p_declColonEqualsInter2(p):
    ''' declColonEqualsInter2 : empty
                              | declColonEqualsInter '''
    p[0] = p[1]

def p_declColonEqualsInter(p):
    ''' declColonEqualsInter : declColonEquals COMMA declColonEqualsInter
                            |  declColonEquals SEMICOLON declColonEqualsInter
                            |  declColonEquals  '''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

    ## original rule : routine = optInd identVis pattern? genericParamList? paramListColon pragma? ('=' COMMENT? stmt)? indAndComment
    ## pattern is used in template hence not implemented

def p_declColonEquals(p) :
    ''' declColonEquals : commaIdentWithPragmaInter commaInter colonTypeDescKInter equalExprInter'''
    # p[0] = { # Not sure what identColonEqualsInter2 does
    # 'vars': p[1],
    # 'type': p[3],
    # 'value': p[4]
    # }
    # for i in p[0]['vars']:
    #     if i in identifierList:
    #     msg_error(p,"Redeclaring Variable \"" + str(i) + "\"")
    #     else:
    #         identifier[i] = {'type': p[3], 'value': p[4]}
    #         identifierList.append(i)

def p_commaIdentWithPragmaInter(p) :
    '''commaIdentWithPragmaInter : identWithPragma
                                  | COMMA identWithPragma commaIdentWithPragmaInter '''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = [p[1]]

def p_commaInter(p): # Not sure what this does
    ''' commaInter : COMMA
                   | empty'''

def p_colonTypeDescKInter(p):
    ''' colonTypeDescKInter : COLON typeDescK
                            | empty '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_equalExprInter(p):
    ''' equalExprInter : EQUALS expr
                            | empty '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_typeDef(p) :
    ''' typeDef : identWithPragma genericParamListInter EQUALS typeDefAux '''

def p_typeDefAux(p) :
    '''  typeDefAux : simpleExpr   '''
    p[0] = p[1]
##  concept not implemented

def p_genericParam(p) :
    '''  genericParam : symbol genericParamInter1 genericParamInter2 genericParamInter3   '''

def p_genericParamInter1(p) :
    ''' genericParamInter1 : COMMA symbol genericParamInter1
                           | empty '''

def p_genericParamInter2(p) :
    ''' genericParamInter2 : COLON expr
                           | empty '''


def p_genericParamInter3(p) :
    ''' genericParamInter3 : EQUALS expr
                           | empty '''

def p_genericParamListInter(p):
    ''' genericParamListInter : genericParamList
                              | empty '''

def p_genericParamList(p):
    '''genericParamList  : BRACKETLE genericParamInter4 optPar BRACKETRI   '''


def p_genericParamInter4(p):
    ''' genericParamInter4 : empty
                              | genericParamInter5 '''

def p_genericParamInter5(p):
    ''' genericParamInter5 : genericParam COMMA genericParamInter5
                            |  genericParam SEMICOLON genericParamInter5
                            |  genericParam  '''


def p_constant(p) :
    ''' constant : identWithPragma constantInter1 EQUALS expr'''

def p_constantInter1(p) :
    ''' constantInter1 : empty
                       | COLON typeKeyww '''

def p_variable(p):
    ''' variable : varTuple
                 | identColonEquals '''
    p[0] = p[1]

def p_varTuple(p) :
    ''' varTuple : PARLE identWithPragma varTupleInter PARRI EQUALS expr '''

def p_varTupleInter(p) :
    ''' varTupleInter : COMMA identWithPragma varTupleInter
                      | empty '''

def p_identColonEquals(p) :
    ''' identColonEquals : identColonEqualsInter1 identColonEqualsInter2 identColonEqualsInter3 identColonEqualsInter4  '''
    p[0] = { # Not sure what identColonEqualsInter2 does
    'vars': p[1],
    'type': p[3],
    'value': p[4]
    }
    for i in p[0]['vars']:
        if i in identifierList:
            msg_error(p,"Redeclaring Variable \"" + str(i) + "\"")
        else:
            identifier[i] = {'type': p[3], 'value': p[4]}
            identifierList.append(i)

def p_identColonEqualsInter1(p) :
    ''' identColonEqualsInter1 : identOrLiteral
                               | COMMA identOrLiteral identColonEqualsInter1'''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = [p[1]]

def p_identColonEqualsInter2(p) :
    ''' identColonEqualsInter2 : empty
                               | COMMA'''

def p_identColonEqualsInter3(p) :
    ''' identColonEqualsInter3 : empty
                               | COLON typeKeyww'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

def p_identColonEqualsInter4(p) :
    ''' identColonEqualsInter4 : empty
                               | EQUALS expr '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

msg = ''

def msg_error(p,_msg=''):
    global msg
    msg = ": " + _msg
    p_error(p)
    msg = ''

def p_error(p):
    global msg
	# global haltExecution
	# haltExecution = True
    try:
		print "Syntax Error near '"+str(p.stack[-1].value)+ "' in line "+str(p.stack[-1].lineno) + str(msg)
    except:
		try:
			print "Syntax Error in line "+str(p.stack[-1].lineno) + str(msg)
		except:
			print "Syntax Error" + str(msg)

	# sys.exit()

# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_

#for epsilon
def p_empty(p):
    'empty :'

    p[0] = {}

# Error rule for syntax errors
# def p_error(p):
#     print("Syntax error!")

# Build the parser
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w")
log = logging.getLogger()
parser = yacc.yacc()

def parseProgram(program):
    parser.parse(program, lexer=lexer)
    pprint(result)

# a function to test the parser
def testYacc(inputFile):
    program = open(inputFile)
    data = program.read()
    customLexer = lexer.customLexer()
    result=parser.parse(data, lexer=customLexer, debug=log)
    pprint(result)
    # parser.parse(program, lexer=lexer, debug=1)

if __name__ == "__main__":
    from sys import argv
    filename, inputFile = argv
    testYacc(inputFile)
    #code to get reduced rules as an output file
    actionfile = open("actionfile.txt", 'w')
    with open("parselog.txt") as f:
        for line in f:
            if line.startswith("INFO:root:Action"):
                actionfile.write(line)
    invert = []
    actionfile = open("actionfile.txt", 'r')
    reverselist = open("reverselist.txt", 'w')
    for line in actionfile:
        rule = re.findall('rule \[(.*)\] with', line)
        if (rule[0]!="empty -> <empty>"):
            reverselist.write(rule[0]+'\n')
            invert.append(rule[0]+'\n')
    #reverselist.txt contains the final production rules
    actionfile.close()
    reverselist.close()
    rulelist = open("rulelist.txt","w")
    while invert:
        rulelist.write(invert.pop())
    rulelist.close()
    #code to create the graphviz flowchart
    nodeno = 1;
    nodes = defaultdict(list)
    data = open(inputFile)
    inputFile = inputFile[0:len(inputFile)-4]
    reverselist = open("reverselist.txt",'r')
    dotfile = open(inputFile+".dot",'w')
    dotfile.write("digraph G {"+"\n graph [ordering=\"out\"];\n")
    for line in reverselist:
        # if "empty -> <empty>" in line: continue
        colsplit = line.split(" ")
        k = len(colsplit)-1
        colsplit[k] = colsplit[k][0:len(colsplit[k])-1]
        pid = nodeno
        innode="node"+str(nodeno)
        dotfile.write(innode+" [ label = \""+colsplit[0]+"\" ];\n")
        nodeno+=1
        for i in range(2,len(colsplit)):
            if colsplit[i] in nodes:
                temp = nodes[colsplit[i]].pop(len(nodes[colsplit[i]])-1)
                outnode="node"+str(temp)
                dotfile.write(innode+" -> "+outnode+";\n")
                if len(colsplit[i])==0:
                    del nodes[colsplit[i]]
            else:
                outnode="node"+str(nodeno)
                dotfile.write(outnode+" [ label = \""+colsplit[i]+"\" ];\n")
                dotfile.write(innode+" -> "+outnode+";\n")
                nodeno+=1
        nodes[colsplit[0]].append(pid)
    dotfile.write("}")

    #code to generate html file
    rulelist = open("rulelist.txt","r")
    final = ["init"]
    lhs = []
    lines = 0
    flag = 0
    for line in rulelist:
        split = line.split(" ")
        lhs.append(split[0])
        lines+=1
    i=1
    html = open("output.html","w")
    rulelist = open("rulelist.txt","r")
    for line in rulelist:
        colsplit = line.split(" ")
        k = len(colsplit)-1
        colsplit[k] = colsplit[k][0:len(colsplit[k])-1]
        html.write('''
<table>
   <tr>
      <td>
        <table>
          <tr>%d. </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>start</tr>
        </table>
      </td>
      <td>
        <table>
           <tr> ==> </tr>
        </table>
      </td>''' %(i))
        final.pop(flag)
        for j in xrange(len(colsplit)-1,1,-1):
            if (colsplit[j]!="empty"):
                final.insert(flag,colsplit[j])

        for j in xrange(len(final)-1,-1,-1):
            if i!=lines:
                if lhs[i]==final[j]:
                    flag=j
                    break
        for j in range(0,len(final)):
            if j!=flag:
                html.write('''
        <td>
            <table>
               <tr> %s </tr>
            </table>
        </td>''' %(final[j]))
            else:
                if i!=lines:
                    html.write('''
        <td>
        <table>
           <tr> <font color="red"><u>%s</u></font></tr>
        </table>
        </td>''' %(final[j]))
                else:
                    html.write('''
        <td>
            <table>
               <tr> %s </tr>
            </table>
        </td>''' %(final[j]))
        html.write('''
    </tr>
</table>''')
        i+=1
