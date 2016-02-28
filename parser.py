#!/usr/bin/python
import ply.yacc as yacc
import logging
import sys, re
from collections import defaultdict
#get tokens
#import lexer #as ourLexer# our lexer
# tokens = lexer.tok_data
import lexer
tokens = lexer.tokens

def p_start(p):
#ignored extra
#module = stmt ^* (';' / IND{=})
    '''start : stmtIndentSemicolon
              | stmt '''

def p_stmtIndentSemicolon(p):
    '''stmtIndentSemicolon : stmt INDEQ stmtIndentSemicolon
                            | stmt SEMICOLON stmtIndentSemicolon
                            | empty'''

def p_stmt(p):
    '''stmt : complexOrSimpleStmt
             | simpleStmt'''

def p_stmtStar(p):
    '''stmtStar : stmt stmtStar
                 | empty'''

def p_suite(p):
    '''suite : simpleStmt
              | INDGR stmt stmtStar INDLE'''


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
    # '''expr : ifExpr
    #         | whenExpr
    #         | simpleExpr'''
    '''expr : simpleExpr'''

# def p_ifExpr(p):
#     '''ifExpr : IF condExpr'''

# def p_whenExpr(p):
#     '''whenExpr : WHEN condExpr'''

def p_simpleExpr(p):
    '''simpleExpr : arrowExpr interOne'''

def p_interOne(p):
    '''interOne : OP0 arrowExpr interOne
                | empty '''

def p_arrowExpr(p):
    '''arrowExpr : assignExpr interTwo'''

def p_interTwo(p):
    '''interTwo : OP1 assignExpr interTwo
                | empty '''

def p_assignExpr(p):
    '''assignExpr : orExpr interThree'''

def p_interThree(p):
    '''interThree : OP2 orExpr interThree
                | empty '''

def p_orExpr(p):
    '''orExpr : andExpr interFour'''

def p_interFour(p):
    '''interFour : OR andExpr interFour
                | XOR andExpr interFour
                | empty '''

def p_andExpr(p):
    '''andExpr : cmpExpr interFive'''

def p_interFive(p):
    '''interFive : AND cmpExpr interFive
                | empty '''

def p_cmpExpr(p):
    '''cmpExpr : sliceExpr interSix'''

def p_interSix(p):
    '''interSix : OP5 sliceExpr interSix
                | empty '''

def p_sliceExpr(p):
    '''sliceExpr : ampExpr interSeven'''

def p_interSeven(p):
    '''interSeven : DOTDOT ampExpr interSeven
                | empty '''

def p_ampExpr(p):
    '''ampExpr : plusExpr interEight'''

def p_interEight(p):
    '''interEight : OP7 plusExpr interEight
                | empty '''

def p_plusExpr(p):
    '''plusExpr : mulExpr interNine'''

def p_interNine(p):
    '''interNine : OP8 mulExpr interNine
                | empty '''

def p_mulExpr(p):
    '''mulExpr : dollarExpr interTen'''

def p_interTen(p):
    '''interTen : OP9 dollarExpr interTen
                | empty '''

def p_dollarExpr(p):
    '''dollarExpr : primary interElev'''

def p_interElev(p):
    '''interElev : OP10 primary interElev
                | empty '''

def p_primary(p):
    '''primary : typeKeyw typeDescK
                | interPrefixOperator identOrLiteral interPrimarySuffix
                | STATIC primary
                | BIND primary'''

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
    '''identOrLiteral : IDENTIFIER'''

def p_typeKeyw(p):
    '''typeKeyw : VAR
                | OUT
                | PTR
                | REF
                | SHARED
                | TUPLE
                | PROC
                | ITERATOR
                | DISTINCT
                | OBJECT
                | ENUM '''

def p_typeDescK(p):
    '''typeDescK : simpleExpr'''

def p_primarySuffix(p):
    '''primarySuffix : doBlocks'''

def p_prefixOperator(p):
    '''prefixOperator : operator'''

# def p_symbol
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
                | NIL'''
# def p_par(p):

def p_doBlocks(p):
    '''doBlocks : doBlock'''

def p_doBlock(p):
    '''doBlock : DO COLON stmt'''
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
                | IN
                | NOTIN
                | OF
                | DIV
                | MOD
                | SHL
                | SHR
                | NOT
                | STATIC
                | DOTDOT'''
# def p_
# def p_
# def p_
# def p_
# def p_
#
#
# def p_condExpr
# def p_op0(p):
# def p_op1
# def p_op2
# def p_op3
# def p_op4
# def p_op5
# def p_op6
# def p_op7
# def p_op8
# def p_op9
# def p_op10
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
# def p_
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
def p_error(p):
    print("Syntax error!")

# Build the parser
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w")
log = logging.getLogger()
parser = yacc.yacc()

def parseProgram(program):
    parser.parse(program, lexer=lexer)
    print(result)

# a function to test the parser
def testYacc(inputFile):
    program = open(inputFile)
    data = program.read()
    customLexer = lexer.customLexer()
    result=parser.parse(data, lexer=customLexer, debug=log)
    print result
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
    reverse = []
    actionfile = open("actionfile.txt", 'r')
    for line in actionfile:
        rule = re.findall('rule \[(.*)\] with', line)
        reverse.append(rule[0])
    #rulelist.txt contains the final production rules 
    rulelist = open("rulelist.txt", 'w')
    while (reverse):
        temp = reverse.pop()
        rulelist.write(temp+'\n')
    actionfile.close()
    rulelist.close()

    #code to create the graphviz flowchart
    lineno = 1;
    nodeno = 1;
    nodes = {}
    data = open(inputFile)
    inputFile = inputFile[0:len(inputFile)-4]
    rulelist = open("rulelist.txt",'r')
    dotfile = open(inputFile+".dot",'w')
    dotfile.write("strict digraph G {"+"\n\n")
    for line in rulelist:
        colsplit = line.split(" ")
        if (len(colsplit)<=3):
            colsplit[2] = colsplit[2][0:len(colsplit[2])-1]
        else:
            k = len(colsplit)-1
            colsplit[k] = colsplit[k][0:len(colsplit[k])-1]
        nodes[colsplit[0]]=nodeno
        nodeno+=1
        for i in range(1,len(colsplit)):
            try:
                temp = nodes[colsplit[i]]
            except KeyError:
                nodes[colsplit[i]]=nodeno
                nodeno+=1
        innode="node"+str(nodes[colsplit[0]])
        dotfile.write(innode+" [ label = \""+colsplit[0]+"\" ];\n")
        for i in range(2,len(colsplit)):
            outnode="node"+str(nodes[colsplit[i]])
            dotfile.write(outnode+" [ label = \""+colsplit[i]+"\" ];\n")
            dotfile.write(innode+" -> "+outnode+";\n")
    dotfile.write("}")






