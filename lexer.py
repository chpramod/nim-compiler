#!/usr/bin/python
from ply import lex
#from helpers import debug as debug

########################################
############# RESERVED #################
########################################
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

########################################
############# TOKENS ###################
########################################
tokens = [
        'DIGIT','HEXDIGIT', 'OCTDIGIT' , 'BINDIGIT', 'HEX_LIT', 'DEC_LIT', 'OCT_LIT', 'BIN_LIT', 'EXPONENT', 'SYM_CHARS', 'SYM_START_CHARS', 'INVALID', 'EOF', 'SYMBOL',
         'INTLIT', 'INT8LIT', 'INT16LIT', 'INT32LIT', 'INT64LIT', 'UINTLIT', 'UINT8LIT',
        'UINT16LIT', 'UINT32LIT', 'UINT64LIT', 'FLOATLIT', 'FLOAT32LIT', 'FLOAT64LIT', 'FLOAT128LIT', 'STRLIT', 'RSTRLIT', 'TRIPLESTRLIT', 'PARLE', 'PARRI',
        'BRACKETLE', 'BRACKETRI', 'CURLYLE', 'CURLYRI', 'BRACKETDOTLE', 'BRACKETDOTRI', 'CURLYDOTLE', 'CURLYDOTRI', 'PARDOTLE', 'PARDOTRI', 'COMMA', 'SEMICOLON',   
        'COLON', 'COLONCOLON', 'EQUALS', 'DOT', 'DOTDOT', 'OPR', 'COMMENT', 'ACCENT', 'IDENTIFIER', 'NUMBER', 'NEWLINE', 'WS'
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


########################################
############# COMMENTS #################
########################################
def t_COMMENT(t):
    r"[ ]*\043[^\n]*"  # \043 is '#'
    pass

# Whitespace
def t_WS(t):
    r' [ ]+ '
    #if t.lexer.at_line_start and t.lexer.paren_count == 0:
    return t

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
    return t

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

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

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



########################################
############# ERROR ####################
########################################
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

######################################################################################################
# Create a lexer which uses the above defined rules, this can be used by the any parser which
# includes this file

######### Required Globals #############
#debug = debug.Debug()
lexer = lex.lex()
prev = 0
########################################

data = '''
!3=4+10$~abcd
 =20
 '''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
# # A function to test the lexer
# def testLex(inputFile):
#     # Open the passed argument as an input file and then pass it to lex
#     program = open(inputFile).read()
#     lexer.input(program)

#     # This iterates over the function lex.token and converts the returned object into an iterator
#     print "\tTYPE \t\t\t\t\t\t VALUE"
#     print "\t---- \t\t\t\t\t\t -----"
#     for tok in iter(lexer.token, None):
#         print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))

# if __name__ == "__main__":
#     from sys import argv
#     filename, inputFile = argv
#     testLex(inputFile)

                                      
        # DIGIT           = r'([0-9])'
        # HEXDIGIT        = r'({DIGIT}|[A-F]|[a-f])'
        # OCTDIGIT        = r'([0-7])'
        # BINDIGIT        = r'([0-1])'
        # HEX_LIT         = r'(0(x|X){HEXDIGIT}(_{HEXDIGIT})*)'
        # DEC_LIT         = r'(-?{DIGIT}(_{DIGIT})*)'
        # OCT_LIT         = r'(0o{OCTDIGIT}(_{OCTDIGIT})*)'
        # BIN_LIT         = r'(0(b|B){BINDIGIT}(_{BINDIGIT})*)'
        # EXPONENT        = r'((e|E)[+-]{DIGIT}(_{DIGIT})*)'
        # SYM_CHARS       = r'([a-zA-Z0-9\x80-\xFF_]+)'
        # SYM_START_CHARS = r'([a-zA-Z\x80-\xFF]+)'
        # //////////////////////////////////////////////////////////////////////////////

# //        INVALID       = "tkInvalid"
# //        EOF           = "[EOF]"
#         SYMBOL         = r'({SYM_START_CHARS}{SYM_CHARS}")'
#         INTLIT         = r'({HEX_LIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT}")'
#         INT8LIT        = r'({INTLIT}'[iI]8")'
#         INT16LIT       = r'({INTLIT}'[iI]16")'
#         INT32LIT       = r'({INTLIT}'[iI]32")'
#         INT64LIT       = r'({INTLIT}'[iI]64")'
#         UINTLIT        = r'({INTLIT}'[uU]")'
#         UINT8LIT       = r'({UINTLIT}'[uU]8")'
#         UINT16LIT      = r'({INTLIT}'[uU]16")'
#         UINT32LIT      = r'({INTLIT}'[uU]32")'
#         UINT64LIT      = r'({INTLIT}'[uU]64")'
#         FLOATLIT       = r'(-?{DIGIT}(_{DIGIT})*((.(_{DIGIT})*[EXPONENT])|{EXPONENT})")'
#         FLOAT32LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]32")'
#         FLOAT64LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]64")'
#         FLOAT128LIT    = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]128")'
#         STRLIT         = r'("(\\"|\\[^"]|[^\\])*")'
#         RSTRLIT        = r'(r{STRLIT}")'
#         TRIPLESTRLIT   = r'(\"""(.|{EOL})*\""")'
# //        GSTRLIT        = "tkGStrLit"
# //        GTRIPLESTRLIT  = "tkGTripleStrLit"
# //        CHARLIT        = "tkCharLit"
#         DIGIT           = r'([0-9])'
#         HEXDIGIT        = r'({DIGIT}|[A-F]|[a-f])'
#         OCTDIGIT        = r'([0-7])'
#         BINDIGIT        = r'([0-1])'
#         HEX_LIT         = r'(0(x|X){HEXDIGIT}(_{HEXDIGIT})*)'
#         DEC_LIT         = r'(-?{DIGIT}(_{DIGIT})*)'
#         OCT_LIT         = r'(0o{OCTDIGIT}(_{OCTDIGIT})*)'
#         BIN_LIT         = r'(0(b|B){BINDIGIT}(_{BINDIGIT})*)'
#         EXPONENT        = r'((e|E)[+-]{DIGIT}(_{DIGIT})*)'
#         SYM_CHARS       = r'([a-zA-Z0-9\x80-\xFF_]+)'
#         SYM_START_CHARS = r'([a-zA-Z\x80-\xFF]+)'
        
# #        INVALID       = "tkInvalid"
# #        EOF           = "[EOF]"
#         SYMBOL         = r'({SYM_START_CHARS}{SYM_CHARS}")'
#         INTLIT         = r'({HEX_LIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT}")'
#         INT8LIT        = r'({INTLIT}'[iI]8")'
#         INT16LIT       = r'({INTLIT}'[iI]16")'
#         INT32LIT       = r'({INTLIT}'[iI]32")'
#         INT64LIT       = r'({INTLIT}'[iI]64")'
#         UINTLIT        = r'({INTLIT}'[uU]")'
#         UINT8LIT       = r'({UINTLIT}'[uU]8")'
#         UINT16LIT      = r'({INTLIT}'[uU]16")'
#         UINT32LIT      = r'({INTLIT}'[uU]32")'
#         UINT64LIT      = r'({INTLIT}'[uU]64")'
#         FLOATLIT       = r'(-?{DIGIT}(_{DIGIT})*((.(_{DIGIT})*[EXPONENT])|{EXPONENT})")'
#         FLOAT32LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]32")'
#         FLOAT64LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]64")'
#         FLOAT128LIT    = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]128")'
#         STRLIT         = r'("(\\"|\\[^"]|[^\\])*")'
#         RSTRLIT        = r'(r{STRLIT}")'
#         TRIPLESTRLIT   = r'(\"""(.|{EOL})*\""")'
#        GSTRLIT        = "tkGStrLit"
#        GTRIPLESTRLIT  = "tkGTripleStrLit"
#        CHARLIT        = "tkCharLit"



        #OPR            = r'([+-*/\\<>!?\^.|=%&$@~:\x80-\xFF]")'
# #        COMMENT        = r'(#[^\r\n]*")'
#         ACCENT         = "`"
# //        INFIXOPR       = "tkInfixOpr"
# //        PREFIXOPR      = "tkPrefixOpr"
# //        POSTFIXOPR     = "tkPostfixOpr"
#     ]

#         OPR            = r'([+-*/\\<>!?\^.|=%&$@~:\x80-\xFF]")'
# #        COMMENT        = r'(#[^\r\n]*")'
#         ACCENT         = "`"
#        INFIXOPR       = "tkInfixOpr"
#        PREFIXOPR      = "tkPrefixOpr"
#        POSTFIXOPR     = "tkPostfixOpr"

# input ::= (SYMBOL|ADDR|AND|AS|ASM|ATOMIC|BIND|BLOCK|BREAK|CASE|CAST|CONCEPT|CONST|CONTINUE|CONVERTER|DEFER|DISCARD|
# DISTINCT|DIV|DO|ELIF|ELSE|END|ENUM|EXCEPT|EXPORT|FINALLY|FOR|FROM|FUNC|GENERIC|IF|IMPORT|IN|INCLUDE|INTERFACE|IS|ISNOT|
# ITERATOR|LET|MACRO|METHOD|MIXIN|MOD|NIL|NOT|NOTIN|OBJECT|OF|OR|OUT|PROC|PTR|RAISE|REF|RETURN|SHL|SHR|STATIC|TEMPLATE|
# TRY|TUPLE|TYPE|USING|VAR|WHEN|WHILE|WITH|WITHOUT|XOR|YIELD|INTLIT|INT8LIT|INT16LIT|INT32LIT|INT64LIT|UINTLIT|UINT8LIT|
# UINT16LIT|UINT32LIT|UINT64LIT|FLOATLIT|FLOAT32LIT|FLOAT64LIT|FLOAT128LIT|STRLIT|RSTRLIT|TRIPLESTRLIT|PARLE|PARRI|
# BRACKETLE|BRACKETRI|CURLYLE|CURLYRI|BRACKETDOTLE|BRACKETDOTRI|CURLYDOTLE|CURLYDOTRI|PARDOTLE|PARDOTRI|COMMA|SEMICOLON|
# COLON|COLONCOLON|EQUALS|DOT|DOTDOT|OPR|COMMENT|ACCENT)*
