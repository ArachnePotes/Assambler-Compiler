# REs made using: https://www.debuggex.com/#cheatsheet

import sly
from rich.console import Console
 
console = Console()

class MegaLexer(sly.Lexer):

    tokens = {

        # Reservado

        STATIC, EXTERN, INT, FLOAT, CHAR, ID,
        CONST, RETURN, BREAK, CONTINUE, IF, ELSE,
        WHILE, FOR, VOID,

        # Operador

        LE, GE, EQ, NE, LAND, LOR,

        # Literales

        INUMBER, FNUMBER, CHARACTER, STRING,

        # Misc

        ELLIPSIS, ADDEQ, SUBEQ, MULEQ, DIVEQ, MODEQ,

    }

    literals = '+-*/&<>!%=;(){}[],'

    # Identificador

    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='
    LAND = r'&&'
    LOR = r'\|\|'
    ELLIPSIS = r'\.\.\.'
    ADDEQ = r'\+='
    SUBEQ = r'-='
    MULEQ = r'\*='
    DIVEQ = r'/='
    MODEQ = r'%='
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    FNUMBER = r'[\+-]?((\d+)\.(\d*))|((\d*)\.(\d+))'
    INUMBER = r'[+-]?\d+'
    CHARACTER = r"'\w'" #
    STRING = r'".*"' 

    # Casos Especiales

    ID['static'] = STATIC
    ID['extern'] = EXTERN
    ID['int'] = INT
    ID['float'] = FLOAT
    ID['char'] = CHAR
    ID['const'] = CONST
    ID['return'] = RETURN
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR

    # Ignore

    ignore = ' \t\r'

    @_(r'//.*\n')
    def ignore_cppcomment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'/\*(|.|\n)*?\*/') 
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_('\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Errores

    @_(r'/\*(.|\n)*')
    def error_close_coment(self, t):
        console.print(f"{self.lineno}: Comentario en bloque sin cierre", justify='center')
        self.lineno += t.value.count('\n')
        self.index += 1

    @_(r"'[^']*$") #
    def error_close_char(self, t):
        console.print(f"{self.lineno}: Caracter sin cierre", justify='center')
        self.lineno += t.value.count('\n')
        self.index += 1

    """ @_(r'"[^"]*$') #
    def error_close_str(self, t):
        console.print(f"{self.lineno}: Cadena sin cierre", justify='center')
        self.lineno += t.value.count('\n')
        self.index += 1 """

    def error(self, t):
        console.print(f"{self.lineno}: Caracter '{t.value[0]}' es ilegal")
        self.index += 1

def pprint(source):
    from rich.table import Table

    lexer = MegaLexer()

    table = Table(title='Mega Lexer: Analizador Léxico')
    table.add_column('Type')
    table.add_column('Value')
    table.add_column('LineNo', justify='rigth')

    for tok in lexer.tokenize(data):
        value = tok.value if isinstance(tok.value, str) else str(tok.value)
        table.add_row(tok.type, tok.value, str(tok.lineno))
        
    console.print(table, justify="center")

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print(f"usage: py {sys.argv[0]} sourcefile")
        exit(1)

    data = open(sys.argv[1], encoding='utf-8').read() #importante el encoding
    pprint(data)