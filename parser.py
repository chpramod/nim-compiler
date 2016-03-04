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

def p_typeDefSuite(p):                         # changed it too
    '''typeDefSuite : typeDef
              | NEWLINE INDGR typeDefStar INDLE'''

def p_typeDefStar(p):                      # changed a bit
    '''typeDefStar : typeDef NEWLINE typeDefStar
                 | typeDef SEMICOLON typeDefStar
                 | typeDef
                 | empty'''

def p_constantSuite(p):                         # changed it too
    '''constantSuite : constant
              | NEWLINE INDGR constantStar INDLE'''

def p_constantStar(p):                      # changed a bit
    '''constantStar : constant NEWLINE constantStar
                 | constant SEMICOLON constantStar
                 | constant
                 | empty'''

def p_variableSuite(p):                         # changed it too
    '''variableSuite : variable
              | NEWLINE INDGR variableStar INDLE'''

def p_variableStar(p):                      # changed a bit
    '''variableStar : variable NEWLINE variableStar
                 | variable SEMICOLON variableStar
                 | variable
                 | empty'''


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
                | exprStmt'''

## we are not implementing exportStmt

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

def p_oprInter(p):
    #should be opr
    '''oprInter : empty'''

def p_forStmt(p):
    '''forStmt : FOR identWithPragma identWithPragmaInter IN expr COLON suite'''

def p_tryStmt(p):
    '''tryStmt : TRY COLON suite exceptInter finallyInter'''

def p_exceptInter(p):
    '''exceptInter : EXCEPT expr COLON suite exceptInter
                   | empty'''

def p_finallyInter(p):
    '''finallyInter : FINALLY COLON suite
                    | empty'''

def p_ifStmt(p):
    '''ifStmt : IF condStmt elifStmt elseStmt'''

def p_whenStmt(p):
    '''whenStmt : WHEN condStmt elifStmt elseStmt'''

def p_condStmt(p):
    '''condStmt : expr COLON suite'''

def p_elseStmt(p):
    '''elseStmt : ELSE COLON suite
                    | empty'''
def p_elifStmt(p):
    '''elifStmt : ELIF condStmt elifStmt
                    | empty'''

def p_exprList(p):
    '''exprList : expr COMMA exprList
                | expr'''

def p_ofBranch(p):
    '''ofBranch : OF exprList COLON suite'''

def p_ofBranches(p):
    '''ofBranches : ofBranch ofBranches elifStmt elseStmt
                    | empty'''

def p_caseStmt(p):
    '''caseStmt : CASE expr COLON NEWLINE INDGR ofBranch ofBranches INDLE'''

def p_echoStmt(p):
    '''echoStmt : ECHO exprList'''

def p_importStmt(p):
    '''importStmt : IMPORT exprList
                | IMPORT expr EXCEPT exprList'''

def p_includeStmt(p):
     '''includeStmt : INCLUDE exprList''' # should be list of IDENTIFIER instead of exprList

def p_fromStmt(p):
     '''fromStmt : FROM IDENTIFIER IMPORT exprList'''

def p_returnStmt(p):
    '''returnStmt : RETURN expr
                | RETURN'''

def p_raiseStmt(p):
    '''raiseStmt : RAISE expr
                | RAISE'''

def p_yieldStmt(p):
    '''yieldStmt : YIELD expr
                | YIELD'''

def p_discardStmt(p):
    '''discardStmt : DISCARD expr
                | DISCARD'''

def p_breakStmt(p):
    '''breakStmt : BREAK expr
                | BREAK'''

def p_continueStmt(p):
    '''continueStmt : CONTINUE expr
                | CONTINUE'''

def p_blockStmt(p):
    '''blockStmt : BLOCK symbol COLON suite
                | BLOCK COLON suite'''

def p_staticStmt(p):
    '''staticStmt : STATIC COLON suite'''

def p_deferStmt(p):
    '''deferStmt : DEFER COLON suite'''

def p_asmStmt(p):
    '''asmStmt : ASM pragma strings
                | ASM strings'''

def p_strings(p):
    '''strings : STRLIT
                | RSTRLIT
                | TRIPLESTRLIT'''

def p_expr(p):
    '''expr : ifExpr
            | whenExpr
            | simpleExpr'''

def p_ifExpr(p):
    '''ifExpr : IF condExpr elifExpr elseExpr'''

def p_whenExpr(p):
    '''whenExpr : WHEN condExpr elifExpr elseExpr'''

def p_condExpr(p):
    '''condExpr : expr COLON expr'''

def p_elifExpr(p):
    '''elifExpr : ELIF expr COLON expr elifExpr
        | empty'''

def p_elseExpr(p):
     '''elseExpr : ELSE COLON expr
        | empty'''

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

def p_castExpr(p):
    '''castExpr : CAST BRACKETLE simpleExpr BRACKETRI PARLE expr PARRI'''

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

def p_identOrLiteral(p):
    # '''identOrLiteral : symbol
    #                   | literal
    #                   | par
    #                   | IDENTIFIER'''
    '''identOrLiteral : IDENTIFIER
                        | literal
                        | castExpr
                        | arrayConstr
                        | tupleConstr
                        | symbol '''

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
                | PROC
                | ITERATOR
                | DISTINCT
                | OBJECT
                | ENUM
                | INT
                | FLOAT
                | CHAR
                | STRING '''

def p_typeDescK(p):
    '''typeDescK : simpleExpr
                 | empty'''

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
                | strings
                | NIL'''
# def p_par(p):

def p_doBlocks(p):
    '''doBlocks : doBlock NEWLINE doBlocks
                | empty '''

def p_doBlock(p):
    '''doBlock : DO COLON suite'''
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

def p_routine(p):
    ''' routine : identVis paramListColon EQUALS suite '''

def p_typeKeyww(p):
    ''' typeKeyww   :     INT
                        | FLOAT
                        | CHAR
                        | STRING '''

def p_paramListColon(p):
    ''' paramListColon : paramListInter
                        | paramListInter COLON typeKeyww'''

def p_paramListInter(p):
    ''' paramListInter : PARLE declColonEqualsInter2 PARRI'''

def p_declColonEqualsInter2(p):
    ''' declColonEqualsInter2 : empty
                              | declColonEqualsInter '''

def p_declColonEqualsInter(p):
    ''' declColonEqualsInter : declColonEquals COMMA declColonEqualsInter
                            |  declColonEquals SEMICOLON declColonEqualsInter
                            |  declColonEquals  '''


    ## original rule : routine = optInd identVis pattern? genericParamList? paramListColon pragma? ('=' COMMENT? stmt)? indAndComment
    ## pattern is used in template hence not implemented


def p_declColonEquals(p) :
    ''' declColonEquals : identWithPragma commaIdentWithPragmaInter commaInter colonTypeDescKInter equalExprInter'''


def p_commaIdentWithPragmaInter(p) :
    '''commaIdentWithPragmaInter : empty
                                  | COMMA identWithPragma commaIdentWithPragmaInter '''


def p_commaInter(p):
    ''' commaInter : COMMA
                   | empty'''

def p_colonTypeDescKInter(p):
    ''' colonTypeDescKInter : COLON typeKeyww
                            | empty '''

def p_equalExprInter(p):
    ''' equalExprInter : EQUALS expr
                            | empty '''
def p_typeDef(p) :
    ''' typeDef : identWithPragma genericParamListInter EQUALS typeDefAux '''

def p_typeDefAux(p) :
    '''  typeDefAux : simpleExpr   '''
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

def p_varTuple(p) :
    ''' varTuple : PARLE identWithPragma varTupleInter PARRI EQUALS expr '''

def p_varTupleInter(p) :
    ''' varTupleInter : COMMA identWithPragma varTupleInter
                      | empty '''

def p_identColonEquals(p) :
    ''' identColonEquals : identOrLiteral identColonEqualsInter1 identColonEqualsInter2 identColonEqualsInter3 identColonEqualsInter4  '''

def p_identColonEqualsInter1(p) :
    ''' identColonEqualsInter1 : empty
                               | COMMA identOrLiteral identColonEqualsInter1'''

def p_identColonEqualsInter2(p) :
    ''' identColonEqualsInter2 : empty
                               | COMMA'''

def p_identColonEqualsInter3(p) :
    ''' identColonEqualsInter3 : empty
                               | COLON typeKeyww'''

def p_identColonEqualsInter4(p) :
    ''' identColonEqualsInter4 : empty
                               | EQUALS expr '''

def p_error(p):
# 	global haltExecution
# 	haltExecution = True
	try:
		print "Syntax Error near '"+str(p.value)+ "' in line "+str(p.lineno)
	except:
		try:
			print "Syntax Error in line "+str(p.lineno)
		except:
			print "Syntax Error"
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
                html.write('''
        <td>
        <table>
           <tr> <font color="red"><u>%s</u></font></tr>
        </table>
        </td>''' %(final[j]))
        html.write('''
    </tr>
</table>''')
        i+=1