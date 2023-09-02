
# CONSTANTS

DIGITS = '0123456789'

# TOKENS
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_AUTOR = 'autor'
TT_FECHA_NAC = 'fecha_nac'
TT_TUTOR = 'tutor'
TT_NOTA = 'nota'
TT_TFC = 'tfc'
TT_TITULO = 'titulo'
TT_EOF = 'EOF'

#NOTAS NO NUMERICAS

NN_A = 'sobresaliente'
NN_B = 'notable'
NN_D = 'aprobado'
NN_E = 'suspenso'
NN_M = 'matricula'



class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name} : {self.details}'
        result += f'\nFile {self.pos_start.fn} , Line {self.pos_start.ln + 1}'
        #result += '\n\n' + string_with_arrows(self.pos_start.ftxt,self.pos_start,self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,"Illegal Character", details)


# POSITION
class Position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    def advance(self,current_char = None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)
    

class Token:
    def __init__(self,type_,value = None,pos_start = None, pos_end= None):
        self.type = type_
        self.value = value 
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    

# LEXER

class Lexer:
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1,fn,text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ['\t','\n','#',' ','<','/','>']:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_numbers())
            elif self.current_char in ('a u t o r').split(" "):
                tokens.append(Token(TT_AUTOR,pos_start=self.pos))
                self.advance()
            elif self.current_char in ('f e c h a _ n a c').split(" "):
                tokens.append(Token(TT_FECHA_NAC,pos_start=self.pos))
                self.advance()
            elif self.current_char in ('t i t u l o').split(" "):
                tokens.append(Token(TT_TITULO,pos_start=self.pos))
                self.advance()
            elif self.current_char in ('t u t o r').split(" "):
                tokens.append(Token(TT_TUTOR,pos_start=self.pos))
                self.advance()
            elif self.current_char in ('n o t a').split(" "):
                tokens.append(Token(TT_NOTA,pos_start=self.pos))
                self.advance()
            elif self.current_char in ('t f c').split(" "):
                tokens.append(Token(TT_TFC,pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,"'" + char + "'")
        tokens.append(Token(TT_EOF,pos_start=self.pos))      
        return tokens,None
    
    def make_numbers(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT,int(num_str),pos_start,self.pos)
        else:
            return Token(TT_FLOAT,float(num_str),pos_start,self.pos)



def run(fn,text):
    lexer = Lexer(fn,text)
    tokens,errors = lexer.make_tokens()
    if errors: return None,errors

    return tokens , errors


