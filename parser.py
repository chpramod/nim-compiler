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
    '''start : stmtIndentSemicolon ENDMARKER
              | stmt ENDMARKER'''

def p_stmtIndentSemicolon(p):
    '''stmtIndentSemicolon : stmt NEWLINE stmtIndentSemicolon
                            | stmt SEMICOLON stmtIndentSemicolon
                            | empty'''

def p_stmt(p):
    '''stmt : complexOrSimpleStmt
             | simpleStmt'''

def p_stmtStar(p):                      # changed a bit
    '''stmtStar : stmt NEWLINE stmtStar
                 | stmt SEMICOLON stmtStar
                 | stmt
                 | empty'''

def p_suite(p):                         # changed it too
    '''suite : simpleStmt
              | NEWLINE INDGR stmtStar INDLE'''


def p_complexOrSimpleStmt(p):
    '''complexOrSimpleStmt : ifStmt
                            | whenStmt
                            | whileStmt
                            | forStmt
                            | simpleStmt '''

def p_simpleStmt(p):
    '''simpleStmt : exprStmt'''

def p_exprStmt(p):
    '''exprStmt : simpleExpr EQUALS expr '''

def p_whileStmt(p):
    '''whileStmt : WHILE condStmt'''

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

def p_optpar(p):
    '''optPar : NEWLINE
              | NEWLINE INDGR
              | empty'''

def p_identVis(p):
    '''identVis : symbol oprInter'''

def p_oprInter(p):
    #should be opr
    '''oprInter : empty'''

def p_forStmt(p):
    '''forStmt : FOR identWithPragma identWithPragmaInter IN expr COLON suite'''

def p_tryStmt(p):
    '''tryStmt : TRY COLON suite'''

def p_ifStmt(p):
    '''ifStmt : IF condStmt
                | IF condStmt ELSE COLON suite'''

def p_whenStmt(p):
    '''whenStmt : WHEN condStmt
                | WHEN condStmt ELSE COLON suite'''

def p_condStmt(p):
    '''condStmt : expr COLON suite'''

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
                | identOrLiteral interPrimarySuffix
                | STATIC primary
                | BIND primary'''
#shd be interPrefixOperator identOrLiteral interPrimarySuffix

def p_interPrefixOperator(p):
    '''interPrefixOperator : prefixOperator interPrefixOperator
                            | empty '''

def p_interPrimarySuffix(p):
    '''interPrimarySuffix : primarySuffix interPrimarySuffix
                            | empty '''

def p_identOrLiteral(p):                    # Revant's question :
                                            # why not literals ?
                                            # we can compare with numbers
    # '''identOrLiteral : symbol
    #                   | literal
    #                   | par
    #                   | IDENTIFIER'''
    '''identOrLiteral : IDENTIFIER
                        | literal'''

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

def p_symbol(p):
    '''symbol : IDENTIFIER
                | ADDR
                | TYPE'''

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
    rulelist = open("rulelist.txt", 'w')
    for line in actionfile:
        rule = re.findall('rule \[(.*)\] with', line)
        rulelist.write(rule[0]+'\n')
    #rulelist.txt contains the final production rules
    actionfile.close()
    rulelist.close()

    #code to create the graphviz flowchart
    nodeno = 1;
    nodes = defaultdict(list)
    data = open(inputFile)
    inputFile = inputFile[0:len(inputFile)-4]
    rulelist = open("rulelist.txt",'r')
    dotfile = open(inputFile+".dot",'w')
    dotfile.write("digraph G {"+"\n graph [ordering=\"out\"];\n")
    for line in rulelist:
        if "empty -> <empty>" in line: continue
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
