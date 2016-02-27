#!/usr/bin/python
import ply.yacc as yacc

#get tokens
import lexer # our lexer
tokens = lexer.tokens

def p_start(p):
#ignored extra
#module = stmt ^* (';' / IND{=})
    '''start : stmt'''

def p_stmt(p):
    '''stmt : complexOrSimpleStmt
             | simpleStmt'''

def p_complexOrSimpleStmt(p):
    '''complexOrSimpleStmt : ifStmt
                            | whenStmt
                            | simpleStmt '''

def p_simpleStmt(p):
    '''simpleStmt : exprStmt'''

def p_exprStmt(p):
    '''exprStmt : simpleExpr EQUALS expr '''

def p_ifStmt(p):
    '''ifStmt : IF condStmt'''

def p_whenStmt(p):
    '''whenStmt : WHEN condStmt'''

def p_condStmt(p):
    '''condStmt : expr COLON stmt'''

def p_expr(p):
    '''expr : ifExpr | whenExpr | simpleExpr'''

def p_ifExpr(p):
    '''ifExpr : IF condExpr'''

def p_whenExpr(p):
    '''whenExpr : WHEN condExpr'''

simpleExpr = arrowExpr (OP0 optInd arrowExpr)*
arrowExpr = assignExpr (OP1 optInd assignExpr)*
assignExpr = orExpr (OP2 optInd orExpr)*
orExpr = andExpr (OP3 optInd andExpr)*
andExpr = cmpExpr (OP4 optInd cmpExpr)*
cmpExpr = sliceExpr (OP5 optInd sliceExpr)*
sliceExpr = ampExpr (OP6 optInd ampExpr)*
ampExpr = plusExpr (OP7 optInd plusExpr)*
plusExpr = mulExpr (OP8 optInd mulExpr)*
mulExpr = dollarExpr (OP9 optInd dollarExpr)*
dollarExpr = primary (OP10 optInd primary)*

def p_simpleExpr(p):
    '''simpleExpr : arrowExpr'''
def p_condExpr
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_
def p_

#for epsilon
def p_empty(p):
    'empty :'

    p[0] = {}

# Error rule for syntax errors
def p_error(p):
    print("Syntax error!")

# Build the parser
parser = yacc.yacc()
