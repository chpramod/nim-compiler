#!/usr/bin/python
from ply import lex
import sys
#from helpers import debug as debug

#run as python lexer.py grtngs.nim
#TO DO:
# 1. Indentation
# 2. Decimals
# 3. Strings
# 4. For integers, currently integers like 5i16 are unaccounted for



#reserved keywords
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

#Clubbing with Tokens
tokens = [
        'DIGIT','HEXDIGIT', 'OCTDIGIT' , 'BINDIGIT', 'HEX_LIT', 'DEC_LIT', 'OCT_LIT', 'BIN_LIT', 'EXPONENT', 'SYM_CHARS', 'SYM_START_CHARS', 'INVALID', 'EOF', 'SYMBOL',
         'INTLIT', 'INT8LIT', 'INT16LIT', 'INT32LIT', 'INT64LIT', 'UINTLIT', 'UINT8LIT',
        'UINT16LIT', 'UINT32LIT', 'UINT64LIT', 'FLOATLIT', 'FLOAT32LIT', 'FLOAT64LIT', 'FLOAT128LIT', 'STRLIT', 'RSTRLIT', 'TRIPLESTRLIT', 'PARLE', 'PARRI',
        'BRACKETLE', 'BRACKETRI', 'CURLYLE', 'CURLYRI', 'BRACKETDOTLE', 'BRACKETDOTRI', 'CURLYDOTLE', 'CURLYDOTRI', 'PARDOTLE', 'PARDOTRI', 'COMMA', 'SEMICOLON',   
        'COLON', 'COLONCOLON', 'EQUALS', 'DOT', 'DOTDOT', 'OPR', 'COMMENT', 'MULTICOMMENT', 'ACCENT', 'IDENTIFIER', 'NUMBER', 'BOOLEAN', 'NEWLINE', 'WS', 'WSI'
        ] + list(reserved.values())

#Delimiters
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



#for passing on comments

def t_MULTICOMMENT(t):
    r"[\s ]*\#\[[^\]]*[^\#]*\]\#\n"
    pass

def t_COMMENT(t):
    r"[\s ]*\#[^\n]*\n"  # \043 is '#'
    pass

########################################
############# LINE NUMBER ##############
########################################
# def t_newline(t):
#     r'\n+'
#     global prev
#     t.lexer.lineno += prev
#     prev = len(t.value)
#     debug.setPrev(prev)
#     debug.setLineNumber(t.lexer.lineno)
# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    #strt = True
    return t


# Whitespace
def t_WSI(t):
    r' ((?<=\n)[\s ]+)|(^[\t]+) '
    #if t.lexer.at_line_start and t.lexer.paren_count == 0:
    return t

# Whitespace
def t_WS(t):
    r' [\s ]+ '
    pass


########################################
############# WHITESPACE ###############
########################################
#t_ignore_WHITESPACE = r"\s"

########################################
############# TYPES ####################
########################################

def t_OPR(t):
    r"\+|"r"-|"r"\*|"r"/|"r"\\|"r"\<|"r"\>|"r"\!|"r"\?|"r"\^|"r"\||"r"\%|"r"\&|"r"\$|"r"\@|"r"\~"
    return t
    
# def t_STRING(t):
#     r"(?P<start>\"|')[^\"']*(?P=start)"
#     t.value = t.value.replace("\"", "").replace("'", "")
#     return t


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
    r'r(\"[^(\")]*\")'  # I think this is right ...
    #r''
    #t.value=t.value[1:-1].decode("string-escape") # .swapcase() # for fun
    return t

def t_STRLIT(t):
    r'"([^\n\\"]+|\\"|\\\\)*"'  # I think this is right ...
    #r''
    #t.value=t.value[1:-1].decode("string-escape") # .swapcase() # for fun
    return t

def t_EXPONENT(t):
	r'([e|E][+-][0-9]+)'
	return t;

def t_BOOLEAN(t):
    r"true|false"
    return t

########################################
############# IDENTIFIER ###############
########################################
def t_IDENTIFIER(t):
    r"[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t


# def t_SYM_CHARS(t):
# 	r'([a-zA-Z0-9\x80-\xFF_]+)'
# 	return t

# def t_SYM_START_CHARS(t):
# 	r'([a-zA-Z\x80-\xFF]+)'
# 	return t

#SYMBOL         = r'({SYM_START_CHARS}{SYM_CHARS}")'
 
#INTLIT         = r'((0(x|X)[0-9A-Fa-f]+)|(0(o|O)[0-7]+)|(0(b|B)[0-1]]+)|\d+)'
#INT8LIT        = r'({INTLIT}'[iI]8")'
#INT16LIT       = r'({INTLIT}'[iI]16")'
#INT32LIT       = r'({INTLIT}'[iI]32")'
#INT64LIT       = r'({INTLIT}'[iI]64")'
#UINTLIT        = r'({INTLIT}'[uU]")'
#UINT8LIT       = r'({UINTLIT}'[uU]8")'
#UINT16LIT      = r'({INTLIT}'[uU]16")'
#UINT32LIT      = r'({INTLIT}'[uU]32")'
#UINT64LIT      = r'({INTLIT}'[uU]64")'
#FLOATLIT       = r'(-?{DIGIT}(_{DIGIT})*((.(_{DIGIT})*[EXPONENT])|{EXPONENT})")'
#FLOAT32LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]32")'
#FLOAT64LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]64")'
#FLOAT128LIT    = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]128")'


########################################
############# ERROR ####################
########################################
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    tok_data.setdefault('ILLEGAL_CHARACTERS', list())
    tok_data['ILLEGAL_CHARACTERS'].append(str(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
prev = 0

with open(sys.argv[1], 'r') as my_file:
    
    lexer.input(my_file.read())

tok_data = {};

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    tok_data.setdefault(tok.type, list())
    tok_data[tok.type].append(str(tok.value));

    print(tok)

print('\n\nTokens\tOccurances\tLexemes\n')
for key,value in tok_data.iteritems():
	print key+"\t\t"+str(len(value))+"\t{"+', '.join(value)+"}"
