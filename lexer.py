#!/usr/bin/python
import lex
import sys
from pprint import pprint

reserved = {
    'addr' : 'ADDR' ,
    'and' : 'AND' ,
    'array' : 'ARRAY',
    'as' : 'AS' ,
    'asm' : 'ASM' ,
    'atomic' : 'ATOMIC' ,
    'bind' : 'BIND' ,
    'block' : 'BLOCK',
    'bool' : 'BOOL' ,
    'break' : 'BREAK' ,
    'case' : 'CASE' ,
    'cast' : 'CAST' ,
    'char' : 'CHAR' ,
    'concept' : 'CONCEPT' ,
    'const' : 'CONST' ,
    'continue' : 'CONTINUE' ,
    'converter' : 'CONVERTER' ,
    'cstring' : 'CSTRING' ,
    'defer' : 'DEFER' ,
    'discard' : 'DISCARD' ,
    'distinct' : 'DISTINCT' ,
    'div' : 'DIV' ,
    'do' : 'DO' ,
    'echo' : 'ECHO',
    'elif' : 'ELIF' ,
    'else' : 'ELSE' ,
    'end' : 'END' ,
    'enum' : 'ENUM' ,
    'except' : 'EXCEPT' ,
    'export' : 'EXPORT' ,
    'finally' : 'FINALLY' ,
    'float' : 'FLOAT' ,
    'float8' : 'FLOAT8' ,
    'float16' : 'FLOAT16' ,
    'float32' : 'FLOAT32' ,
    'float64' : 'FLOAT64' ,
    'for' : 'FOR' ,
    'from' : 'FROM' ,
    'func' : 'FUNC' ,
    'generic' : 'GENERIC' ,
    'if' : 'IF' ,
    'import' : 'IMPORT' ,
    'in' : 'IN' ,
    'include' : 'INCLUDE' ,
    'int' : 'INT' ,
    'int8' : 'INT8' ,
    'int16' : 'INT16' ,
    'int32' : 'INT32' ,
    'int64' : 'INT64' ,
    'interface' : 'INTERFACE' ,
    'is' : 'IS' ,
    'isnot' : 'ISNOT' ,
    'iterator' : 'ITERATOR' ,
    'let' : 'LET' ,
    'macro' : 'MACRO' ,
    'method' : 'METHOD' ,
    'mixin' : 'MIXIN' ,
    'mod' : 'MOD' ,
    'nil' : 'NIL' ,
    'not' : 'NOT' ,
    'notin' : 'NOTIN' ,
    'object' : 'OBJECT' ,
    'of' : 'OF' ,
    'openArray' : 'OPENARRAY' ,
    'or' : 'OR' ,
    'out' : 'OUT' ,
    'proc' : 'PROC' ,
    'ptr' : 'PTR' ,
    'raise' : 'RAISE' ,
    'ref' : 'REF' ,
    'return' : 'RETURN' ,
    'set' : 'SET' ,
    'seq' : 'SEQ' ,
    'shared' : 'SHARED' ,
    'shl' : 'SHL' ,
    'shr' : 'SHR' ,
    'static' : 'STATIC' ,
    'string' : 'STRING' ,
    'template' : 'TEMPLATE' ,
    'try' : 'TRY' ,
    'tuple' : 'TUPLE' ,
    'type' : 'TYPE' ,
    'uint' : "UINT" ,
    'uint8' : "UINT8" ,
    'uint16' : "UINT16" ,
    'uint32' : "UINT32" ,
    'uint64' : "UINT64" ,
    'using' : 'USING' ,
    'var' : 'VAR' ,
    'varargs' : 'VARARGS' ,
    'when' : 'WHEN' ,
    'while' : 'WHILE' ,
    'with' : 'WITH' ,
    'without' : 'WITHOUT' ,
    'xor' : 'XOR' ,
    'yield' : 'YIELD'
}

tokens = [
        'EXPONENT','INTLIT', 'INT8LIT', 'INT16LIT', 'INT32LIT', 'INT64LIT', 'UINTLIT', 'UINT8LIT', 'UINT16LIT', 'UINT32LIT', 'UINT64LIT',
         'FLOATLIT', 'FLOAT32LIT', 'FLOAT64LIT', 'FLOAT128LIT', 'CHARLIT', 'STRLIT', 'RSTRLIT', 'TRIPLESTRLIT', 'PARLE', 'PARRI',
        'BRACKETLE', 'BRACKETRI', 'CURLYLE', 'CURLYRI', 'BRACKETDOTLE', 'BRACKETDOTRI', 'CURLYDOTLE', 'CURLYDOTRI', 'PARDOTLE', 'PARDOTRI', 'COMMA', 'SEMICOLON',
        'COLON', 'COLONCOLON', 'EQUALS', 'DOT', 'DOTDOT', 'OP0', 'OP1', 'OP2', 'OP3', 'OP4', 'OP5', 'OP6', 'OP7', 'OP8', 'OP9', 'OP10', 'COMMENT', 'MULTICOMMENT',
         'ACCENT', 'IDENTIFIER', 'NUMBER', 'BOOLEAN', 'NEWLINE', 'WS', 'WSI', 'INDGR','INDLE','INDEQ', 'ENDMARKER'
        ] + list(reserved.values())

def t_OP0(t):
    r"-\>|"r"=\>"
    return t

def t_OP1(t):
    r"\+=|"r"\*=|"r"\\="

def t_OP2(t):
    r"\?|"r"\@"
    return t

def t_OP5(t):
    r"==|"r"\<=|"r"\>=|"r"\!=|"r"\<|"r"\>|"r"\!"
    return t

def t_OP7(t):
    r"\&"
    return t

def t_OP8(t):
    r"\+|"r"-|"r"\||"r"\~"
    return t

def t_OP9(t):
    r"\*|"r"/|"r"\\|"r"\%"
    return t

def t_OP10(t):
    r"\$|"r"\^"
    return t

t_PARLE          = r'\('
t_PARRI          = r'\)'
t_BRACKETLE      = r'\['
t_BRACKETRI      = r'\]'
t_CURLYLE        = r'\{'
t_CURLYRI        = r'\}'
t_BRACKETDOTLE   = r'\[\.'
t_BRACKETDOTRI   = r'\.\['
t_CURLYDOTLE     = r'\{\.'
t_CURLYDOTRI     = r'\.\}'
t_PARDOTLE       = r'\(\.'
t_PARDOTRI       = r'\.\)'
t_COMMA          = r'\,'
t_SEMICOLON      = r';'
t_COLON          = r':'
t_COLONCOLON     = r'::'
t_EQUALS         = r'='
t_DOT            = r'\.'
t_DOTDOT         = r'\.\.'
t_ACCENT         = r'`'

def t_MULTICOMMENT(t):
    r"[\s ]*\#\[[^\]]*[^\#]*\]\#\n"
    pass

def t_COMMENT(t):
    r"[\s ]*\#[^\n]*\n"  # \043 is '#'
    pass

def t_NEWLINE(t):
    r'[\n]+'
    #t.lexer.lineno += len(t.value)
    return t

def t_WSI(t):
    r' ((?<=\n)[\s ]+)|(^[\t]+) '
    return t

def t_WS(t):
    r' [\s]'
    return t

# def t_OPR(t):
#     r"\+|"r"-|"r"\*|"r"/|"r"\\|"r"\<|"r"\>|"r"\!|"r"\?|"r"\^|"r"\||"r"\%|"r"\&|"r"\$|"r"\@|"r"\~"
#     return t

def t_CHARLIT(t):
    r"\'((.)|(\\r)|(\\c)|(\\f)|(\\v)|(\\t)|(\\\\)|(\\\")|(\\')|(\\a)|(\\b)|(\\e)|(0(x|X)[0-9A-Fa-f][0-9A-Fa-f])|(\d+))\'"
    return t;

def t_FLOAT32LIT (t) :
    r'(((\d*)\.(\d+)) | ((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+) ) (\'[fF]32)'
    return t

def t_FLOAT64LIT (t) :
    r'(((\d*)\.(\d+)) | ((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+) ) (\'[fF]64)'
    return t

def t_FLOAT128LIT (t) :
    r'(((\d*)\.(\d+)) | ((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+) ) (\'[fF]128)'
    return t

def t_FLOATLIT (t) :
    r'((\d*)\.(\d+))'
    return t

def t_INT64LIT(t):
    r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)\'([iI]64)'
    return t

def t_INT32LIT(t):
    r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)\'([iI]32)'
    return t

def t_INT16LIT(t):
    r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)\'([iI]16)'
    return t

def t_INT8LIT(t):
    r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)\'([iI]8)'
    return t

def t_INTLIT(t):
	r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)'
	return t

# def t_HEX_LIT(t):
# 	r"(0(x|X)[0-9A-Fa-f]+)"
# 	return t

# def t_OCT_LIT(t):
# 	r"(0(o|O)[0-7]+)"
# 	return t

# def t_BIN_LIT(t):
#     r'(0(b|B)[0-1]]+)'
#     t.value = int(t.value)
#     return t

# def t_DEC_LIT(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t

def t_TRIPLESTRLIT(t):
    r'(\"\"\"[^(\"\"\")]*\"\"\")'
    return t

def t_RSTRLIT(t):
    r'r(\"[^(\")]*\")'
    return t

def t_STRLIT(t):
    r'"([^\n\\"]+|\\"|\\\\)*"'

    return t

def t_EXPONENT(t):
	r'([e|E][+-][0-9]+)'
	return t;

def t_BOOLEAN(t):
    r"true|false"
    return t

def t_IDENTIFIER(t):
    r"[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    # tok_data.setdefault('ILLEGAL_CHARACTERS', list())
    tok_data.append(t)
    t.lexer.skip(1)

# lexer = lex.lex()
# prev = 0

# with open(sys.argv[1], 'r') as my_file:

#     lexer.input(my_file.read())

# def indentation(lexer):
#     stack = []
#     stack.append(0);
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break      # No more input
#         tok_data.setdefault(tok.type, list())
#         tok_data[tok.type].append(str(tok.value));
#         if (tok.type == "WSI"):
#             tok.value = len(tok.value)
#             temp = stack.pop()
#             if (tok.value > temp):
#                 tok.type = 'INDGR'
#                 stack.append(temp)
#                 stack.append(tok.value)
#             elif (tok.value == temp):
#                 tok.type = 'INDEQ'
#                 stack.append(temp)
#             else:
#                 tok.type = 'INDLE'
#                 while (tok.value > temp):
#                     yield tok
#                     temp = stack.pop()
def generateIndentation(lexer):
    tok_data = [];
    prev_ind = 0
    next_ind = 0
    lineno = 1
    tok = lexer.token()
    if(tok.type=="WS"):
        t_error(tok)

    # newtok = lex.LexToken()
    # newtok.type = 'INDGR'
    # newtok.value = 1
    # newtok.lexpos = tok.lexpos
    # newtok.lineno = lineno
    # tok_data.append(newtok)

    while True:
        if not tok:
            break      # No more input
        tok.lineno = lineno
        # if 1:
        if not (tok.type=="WSI" or tok.type=="WS" or tok.type=="NEWLINE"):
            tok_data.append(tok)
        nexttok = lexer.token()
        flag=0
        if not nexttok:
            flag=0
        elif nexttok.type=="WSI":
            flag=1
        # tok_data.setdefault(tok.type, list())
        # tok_data[tok.type].append(str(tok.value));
        if (tok.type == "NEWLINE"):
            lineno+=1
            if(flag):
                if(len(nexttok.value)%2==1):
                    t_error(nexttok)
            if (flag):
                next_ind = len(nexttok.value)/2
            else:
                next_ind = 0
            for i in range(0,prev_ind - next_ind):
                newtok = lex.LexToken()
                newtok.type = 'INDLE'
                newtok.value = -1
                newtok.lexpos = tok.lexpos
                newtok.lineno = lineno
                tok_data.append(newtok)
            tok_data.append(tok)
            for i in range(0,next_ind - prev_ind):
                newtok = lex.LexToken()
                newtok.type = 'INDGR'
                newtok.value = 1
                newtok.lexpos = tok.lexpos
                newtok.lineno = lineno
                tok_data.append(newtok)
            # if(next_ind <= prev_ind):
            #     newtok = lex.LexToken()
            #     newtok.type = 'INDEQ'
            #     newtok.value = 0
            #     newtok.lexpos = tok.lexpos
            #     newtok.lineno = lineno
            #     tok_data.append(newtok)
            prev_ind = next_ind
        tok = nexttok

    newtok = lex.LexToken()
    newtok.type = 'ENDMARKER'
    newtok.value = -1
    newtok.lexpos = -1
    newtok.lineno = lineno
    tok_data.append(newtok)

    pprint(tok_data)
    return tok_data
class customLexer(object):
    def __init__(self):
        self.lexer = lex.lex()
        self.tok_data = None
    def input(self,data):
        self.lexer.input(data)
        self.tok_data = iter(generateIndentation(self.lexer))
    def token(self):
        try:
            return self.tok_data.next()
        except StopIteration:
            return None

# cLexer = customLexer()
# data = open(sys.argv[1], 'r').read()
# cLexer.input(data)
# tok = cLexer.token()
# while True:
#     if not tok:
#         break
#     # print tok
#     tok = cLexer.token()


# print('\n\nTokens\tOccurances\tLexemes\n')
# for key,value in tok_data.iteritems():
#     length = len(value)
#     value = list(set(value))
#     if ((key == "WSI") or (key == "NEWLINE")):
#         print '{:8s}'.format(key) + "          "+str(length)
#     else:
#         print '{:8s}'.format(key) +"          "+str(length)+"\n\t\t\t    "+'\n\t\t\t    '.join(value)
