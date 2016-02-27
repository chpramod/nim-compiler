#!/usr/bin/python
import ply.yacc as yacc

#get tokens
import lexer # our lexer
tokens = lexer.tokens


# Error rule for syntax errors
def p_error(p):
    print("Syntax error!")

# Build the parser
parser = yacc.yacc()
