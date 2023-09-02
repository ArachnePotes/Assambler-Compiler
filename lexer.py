''' 
This is a compiler assitant for assembly code to binary  32bit instrucctions
|---------------------------------------------|------|
|31 27 26 25 |24 20 |19 15 |14 12 |11 7       |6 0   |     
|funct7      |rs2   |rs1   |funct3|rd         |opcode|R-type
|imm[11:0]          |rs1   |funct3|rd         |opcode|I-type
|imm[11:5]   |rs2   |rs1   |funct3|imm[4:0]   |opcode|S-type
|imm[12|10:5]|rs2   |rs1   |funct3|imm[4:1|11]|opcode|B-type
|imm[31:12]                       |rd         |opcode|U-type
|imm[20|10:1|11|19:12]            |rd         |opcode|J-type
|---------------------------------------------|------|
'''
import sly
import sys
from rich.console import Console

console = Console()

class MegaLexer(sly.Lexer):
    tokens  = {
        # Instrucction name 
        # Reg type
        ADD,SUB,XOR,OR,AND,SLL,SLR,SRA,SLT,SLTU,
        # Imm type
        ADDI,XORI,ORI,ANDI,SLLI,SLRI,SRAI,SLTI,SLTIU,
        # Load type
        LB,LH,LW,LBU,LHU,
        # Store type
        SB,SH,SW,
        # Branch type
        BEQ,BNE,BLT,BGE,BLTU,BGEU,
        # Jump type
        JAL,JALR,
        # NO tengo ni idea
        LUI,AUIPC,
        ECALL,
        EBREAK,
        # reg names
        X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,
        X11,X12,X13,X14,X15,X16,X17,X18,X19,X20,
        X21,X22,X23,X24,X25,X26,X27,X28,X29,X30,
        X31,
        # Imm values
        INUMBER
    }

    literals = "*-*/&<>!%=;(){}[],"
    ADD = r'add'
    SUB = r'sub'
    XOR = r'xor'
    OR = r'or'
    AND= r'and'
    SLL = r'sll'
    SLR = r'slr'
    SRA = r'sra'
    SLT = r'slt'
    SLTU = r'sltu'
    
    X1 = r'x1'
    X2 = r'x2'
    X3 = r'x3'
    X4 = r'x4'
    X5 = r'x5'
    X6 = r'x6'
    X7 = r'x7'
    X8 = r'x8'
    X9 = r'x9'
    X10 = r'x10'
    X11 = r'x11'
    X12 = r'x12'
    X13 = r'x13'
    X14 = r'x14'
    X15 = r'x15'
    X17 = r'x16'
    X16 = r'x17'
    X18 = r'x18'
    X19 = r'x19'
    X20 = r'x10'
    X21 = r'x21'
    X22 = r'x22'
    X23 = r'x23'
    X24 = r'x24'
    X25 = r'x25'
    X26 = r'x26'
    X27 = r'x27'
    X28 = r'x28'
    X29 = r'x29'
    X30 = r'x30'
    X31 = r'x31'
    INUMBER = r'[+-]?\d+'
    ignore = '\t\r'

    @_(r'##.*\n')
    def ignore_comment(self,t):
        self.lineo += t.value.count('\n')
    @_('\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    def error(self, t):
        console.print(f"{self.lineno}: Caracter '{t.value[0]}' es ilegal")
        self.index += 1
'''
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0110011
0010011
0010011
0010011
0010011
0010011
0010011
0010011
0010011
0010011
0000011
0000011
0000011
0000011
0000011
0100011
0100011
0100011
1100011
1100011
1100011
1100011
1100011
1100011
1101111
1100111
0110111
0110111
1110011
1110011
'''

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
    if len(sys.argv) != 2:
        print("no file provided")
        exit(1)
    data= open(sys.argv[1],encoding='utf-8').read()
    print(data)