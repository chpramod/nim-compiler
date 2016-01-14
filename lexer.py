#Nim-Compiler Lexer file
# lexer.py
#
import ply.lex as lex        // After generating flex lexer delete this section somewhere after <YYINITIAL>

#Token Name list
#Not written the ones with //
tokens = ('DIGIT','HEXDIGIT', 'OCTDIGIT' , 'BINDIGIT', 'HEX_LIT', 'DEC_LIT', 'OCT_LIT', 'BIN_LIT', 'EXPONENT', 'SYM_CHARS', 'SYM_START_CHARS', 'INVALID', 'EOF', 'SYMBOL', 'ADDR', 'AND', 'AS', 'ASM', 'ATOMIC', 'BIND', 'BLOCK', 'BREAK', 'CASE', 'CAST', 'CONCEPT', 'CONST', 'CONTINUE', 'CONVERTER', 'DEFER', 'DISCARD',
	'DISTINCT', 'DIV', 'DO', 'ELIF', 'ELSE', 'END', 'ENUM', 'EXCEPT', 'EXPORT', 'FINALLY', 'FOR', 'FROM', 'FUNC', 'GENERIC', 'IF', 'IMPORT', 'IN', 'INCLUDE', 'INTERFACE', 'IS', 'ISNOT', 
	'ITERATOR', 'LET', 'MACRO', 'METHOD', 'MIXIN', 'MOD', 'NIL', 'NOT', 'NOTIN', 'OBJECT', 'OF', 'OR', 'OUT', 'PROC', 'PTR', 'RAISE', 'REF', 'RETURN', 'SHL', 'SHR', 'STATIC', 'TEMPLATE',
	'TRY', 'TUPLE', 'TYPE', 'USING', 'VAR', 'WHEN', 'WHILE', 'WITH', 'WITHOUT', 'XOR', 'YIELD', 'INTLIT', 'INT8LIT', 'INT16LIT', 'INT32LIT', 'INT64LIT', 'UINTLIT', 'UINT8LIT',
	'UINT16LIT', 'UINT32LIT', 'UINT64LIT', 'FLOATLIT', 'FLOAT32LIT', 'FLOAT64LIT', 'FLOAT128LIT', 'STRLIT', 'RSTRLIT', 'TRIPLESTRLIT', 'PARLE', 'PARRI',
	'BRACKETLE', 'BRACKETRI', 'CURLYLE', 'CURLYRI', 'BRACKETDOTLE', 'BRACKETDOTRI', 'CURLYDOTLE', 'CURLYDOTRI', 'PARDOTLE', 'PARDOTRI', 'COMMA', 'SEMICOLON',	
	'COLON', 'COLONCOLON', 'EQUALS', 'DOT', 'DOTDOT', 'OPR', 'COMMENT', 'ACCENT')                                                                                                                                                                                                                                        

        DIGIT           = r'([0-9])'
        HEXDIGIT        = r'({DIGIT}|[A-F]|[a-f])'
        OCTDIGIT        = r'([0-7])'
        BINDIGIT        = r'([0-1])'
        HEX_LIT         = r'(0(x|X){HEXDIGIT}(_{HEXDIGIT})*)'
        DEC_LIT         = r'(-?{DIGIT}(_{DIGIT})*)'
        OCT_LIT         = r'(0o{OCTDIGIT}(_{OCTDIGIT})*)'
        BIN_LIT         = r'(0(b|B){BINDIGIT}(_{BINDIGIT})*)'
        EXPONENT        = r'((e|E)[+-]{DIGIT}(_{DIGIT})*)'
        SYM_CHARS       = r'([a-zA-Z0-9\x80-\xFF_]+)'
        SYM_START_CHARS = r'([a-zA-Z\x80-\xFF]+)'
        //////////////////////////////////////////////////////////////////////////////

//        INVALID       = "tkInvalid"
//        EOF           = "[EOF]"
        SYMBOL         = r'({SYM_START_CHARS}{SYM_CHARS}")'
        ADDR           = "addr"
        AND            = "and"
        AS             = "as"
        ASM            = "asm"
        ATOMIC         = "atomic"
        BIND           = "bind"
        BLOCK          = "block"
        BREAK          = "break"
        CASE           = "case"
        CAST           = "cast"
        CONCEPT        = "concept"
        CONST          = "const"
        CONTINUE       = "continue"
        CONVERTER      = "converter"
        DEFER          = "defer"
        DISCARD        = "discard"
        DISTINCT       = "distinct"
        DIV            = "div"
        DO             = "do"
        ELIF           = "elif"
        ELSE           = "else"
        END            = "end"
        ENUM           = "enum"
        EXCEPT         = "except"
        EXPORT         = "export"
        FINALLY        = "finally"
        FOR            = "for"
        FROM           = "from"
        FUNC           = "func"
        GENERIC        = "generic"
        IF             = "if"
        IMPORT         = "import"
        IN             = "in"
        INCLUDE        = "include"
        INTERFACE      = "interface"
        IS             = "is"
        ISNOT          = "isnot"
        ITERATOR       = "iterator"
        LET            = "let"
        MACRO          = "macro"
        METHOD         = "method"
        MIXIN          = "mixin"
        MOD            = "mod"
        NIL            = "nil"
        NOT            = "not"
        NOTIN          = "notin"
        OBJECT         = "object"
        OF             = "of"
        OR             = "or"
        OUT            = "out"
        PROC           = "proc"
        PTR            = "ptr"
        RAISE          = "raise"
        REF            = "ref"
        RETURN         = "return"
        SHL            = "shl"
        SHR            = "shr"
        STATIC         = "static"
        TEMPLATE       = "template"
        TRY            = "try"
        TUPLE          = "tuple"
        TYPE           = "type"
        USING          = "using"
        VAR            = "var"
        WHEN           = "when"
        WHILE          = "while"
        WITH           = "with"
        WITHOUT        = "without"
        XOR            = "xor"
        YIELD          = "yield"
        INTLIT         = r'({HEX_LIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT}")'
        INT8LIT        = r'({INTLIT}'[iI]8")'
        INT16LIT       = r'({INTLIT}'[iI]16")'
        INT32LIT       = r'({INTLIT}'[iI]32")'
        INT64LIT       = r'({INTLIT}'[iI]64")'
        UINTLIT        = r'({INTLIT}'[uU]")'
        UINT8LIT       = r'({UINTLIT}'[uU]8")'
        UINT16LIT      = r'({INTLIT}'[uU]16")'
        UINT32LIT      = r'({INTLIT}'[uU]32")'
        UINT64LIT      = r'({INTLIT}'[uU]64")'
        FLOATLIT       = r'(-?{DIGIT}(_{DIGIT})*((.(_{DIGIT})*[EXPONENT])|{EXPONENT})")'
        FLOAT32LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]32")'
        FLOAT64LIT     = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]64")'
        FLOAT128LIT    = r'(({HEX_LIT}|{FLOATLIT}|{DEC_LIT}|{OCT_LIT}|{BIN_LIT})'[fF]128")'
        STRLIT         = r'("(\\"|\\[^"]|[^\\])*")'
        RSTRLIT        = r'(r{STRLIT}")'
        TRIPLESTRLIT   = r'(\"""(.|{EOL})*\""")'
//        GSTRLIT        = "tkGStrLit"
//        GTRIPLESTRLIT  = "tkGTripleStrLit"
//        CHARLIT        = "tkCharLit"
        PARLE          = "("
        PARRI          = ")"
        BRACKETLE      = "["
        BRACKETRI      = "]"
        CURLYLE        = "{"
        CURLYRI        = "}"
        BRACKETDOTLE   = "[."
        BRACKETDOTRI   = ".]"
        CURLYDOTLE     = "{."
        CURLYDOTRI     = ".}"
        PARDOTLE       = "(."
        PARDOTRI       = ".)"
        COMMA          = ","
        SEMICOLON      = ";"
        COLON          = ":"
        COLONCOLON     = "::"
        EQUALS         = "="
        DOT            = "."
        DOTDOT         = ".."
        OPR            = r'([+-*/\\<>!?\^.|=%&$@~:\x80-\xFF]")'
        COMMENT        = r'(#[^\r\n]*")'
        ACCENT         = "`"
//        INFIXOPR       = "tkInfixOpr"
//        PREFIXOPR      = "tkPrefixOpr"
//        POSTFIXOPR     = "tkPostfixOpr"
    ]
}

input ::= (SYMBOL|ADDR|AND|AS|ASM|ATOMIC|BIND|BLOCK|BREAK|CASE|CAST|CONCEPT|CONST|CONTINUE|CONVERTER|DEFER|DISCARD|
DISTINCT|DIV|DO|ELIF|ELSE|END|ENUM|EXCEPT|EXPORT|FINALLY|FOR|FROM|FUNC|GENERIC|IF|IMPORT|IN|INCLUDE|INTERFACE|IS|ISNOT|
ITERATOR|LET|MACRO|METHOD|MIXIN|MOD|NIL|NOT|NOTIN|OBJECT|OF|OR|OUT|PROC|PTR|RAISE|REF|RETURN|SHL|SHR|STATIC|TEMPLATE|
TRY|TUPLE|TYPE|USING|VAR|WHEN|WHILE|WITH|WITHOUT|XOR|YIELD|INTLIT|INT8LIT|INT16LIT|INT32LIT|INT64LIT|UINTLIT|UINT8LIT|
UINT16LIT|UINT32LIT|UINT64LIT|FLOATLIT|FLOAT32LIT|FLOAT64LIT|FLOAT128LIT|STRLIT|RSTRLIT|TRIPLESTRLIT|PARLE|PARRI|
BRACKETLE|BRACKETRI|CURLYLE|CURLYRI|BRACKETDOTLE|BRACKETDOTRI|CURLYDOTLE|CURLYDOTRI|PARDOTLE|PARDOTRI|COMMA|SEMICOLON|
COLON|COLONCOLON|EQUALS|DOT|DOTDOT|OPR|COMMENT|ACCENT)*
