#!/usr/bin/python
import lex
import sys

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
        'COLON', 'COLONCOLON', 'EQUALS', 'DOT', 'DOTDOT', 'OPR', 'COMMENT', 'MULTICOMMENT', 'ACCENT', 'IDENTIFIER', 'NUMBER', 'BOOLEAN', 'NEWLINE', 'WS', 'WSI'
        ] + list(reserved.values())

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
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_WSI(t):
    r' ((?<=\n)[\s ]+)|(^[\t]+) '
    return t

def t_WS(t):
    r' [\s ]+ '
    pass

def t_OPR(t):
    r"\+|"r"-|"r"\*|"r"/|"r"\\|"r"\<|"r"\>|"r"\!|"r"\?|"r"\^|"r"\||"r"\%|"r"\&|"r"\$|"r"\@|"r"\~"
    return t

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

    #print(tok)

print('\n\nTokens\tOccurances\tLexemes\n')
for key,value in tok_data.iteritems():
    length = len(value)
    value = list(set(value))
    if ((key == "WSI") or (key == "NEWLINE")):
        print '{:8s}'.format(key) + "          "+str(length)
    else:
        print '{:8s}'.format(key) +"          "+str(length)+"\n\t\t\t    "+'\n\t\t\t    '.join(value)

