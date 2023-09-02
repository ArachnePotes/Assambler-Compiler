import logging
import sly
from absC import *

from mclexer import MyLexer


class Parser(sly.Parser):
    debugfile = "minic.txt"

    tokens = MyLexer.tokens
    
    @_("translation_unit")
    def program(self, p):
        return TranslationUnit(p.translation_unit)

    @_("external_declaration")
    def translation_unit(self, p):
        return [p.external_declaration]

    @_("translation_unit external_declaration")
    def translation_unit(self, p):
        return p.translation_unit + [p.external_declaration]

    @_("function_definition",
       "declaration")
    def external_declaration(self, p):
        return p[0]

    @_("type_specifier declarator compound_statement")
    def function_definition(self, p):
        if isinstance(p.declarator, Variable):
            return FuncNoParamsDefinition(p.type_specifier, p.declarator, p.compound_statement)
        else:
            return FuncDefinition(p.type_specifier, p.declarator[0], p.declarator[1], p.compound_statement)

    @_("STATIC type_specifier declarator compound_statement")
    def function_definition(self, p):
        if isinstance(p.declarator, Variable):
            return FuncNoParamsDefinition(p.type_specifier, p.declarator, p.compound_statement, True)
        else:
            return FuncDefinition(p.type_specifier, p.declarator[0], p.declarator[1], p.compound_statement, True)

    @_("type_specifier declarator ';'")
    def declaration(self, p):
        return TypeDefinition(p.type_specifier, p.declarator)

    @_("EXTERN type_specifier declarator ';'")
    def declaration(self, p):
        if isinstance(p.declarator, Variable):
            return TypeDefinition(p.type_specifier, p.declarator)
        else:
            return ExternTypeParams(p.type_specifier, p.declarator[0], p.declarator[1])

    @_("CONST type_specifier declarator ';'")
    def declaration(self, p):
        return TypeDefinition(p.type_specifier, p.declarator, False, True)

    @_("empty")
    def declaration_list_opt(self, p):
        return p.empty

    @_("declaration_list")
    def declaration_list_opt(self, p):
        return p.declaration_list

    @_("declaration")
    def declaration_list(self, p):
        return [p.declaration]

    @_("declaration_list declaration")
    def declaration_list(self, p):
        return p.declaration_list + [p.declaration]

    @_("INT", "FLOAT", "CHAR", "VOID")
    def type_specifier(self, p):
        return p[0]

    @_("direct_declarator")
    def declarator(self, p):
        return p.direct_declarator

    @_("'*' declarator")
    def declarator(self, p):
        if isinstance(p.declarator, Variable):
            return Variable(p[0] + p.declarator.name)
        else:
            return (Variable(p[0] + p.declarator[0].name), p.declarator[1])

    @_("ID")
    def direct_declarator(self, p):
        return Variable(p.ID)
# -----

    @_("direct_declarator '(' parameter_type_list ')'")
    def direct_declarator(self, p):
        return p.direct_declarator, p.parameter_type_list

    @_("direct_declarator '(' ')'")
    def direct_declarator(self, p):
        return p.direct_declarator

    @_("parameter_list")
    def parameter_type_list(self, p):
        return p.parameter_list

    @_("parameter_list ',' ELLIPSIS")
    def parameter_type_list(self, p):
        return p.parameter_list + [Ellipsis(p.ELLIPSIS)]

    @_("parameter_declaration")
    def parameter_list(self, p):
        return [p.parameter_declaration]

    @_("parameter_list ',' parameter_declaration")
    def parameter_list(self, p):
        return p.parameter_list + [p.parameter_declaration]

    @_("type_specifier declarator")
    def parameter_declaration(self, p):
        return TypeDefinition(p.type_specifier, p.declarator)

    @_("'{' declaration_list_opt statement_list '}'")
    def compound_statement(self, p):
        return [p.declaration_list_opt] + p.statement_list

    @_("'{' declaration_list_opt '}'")
    def compound_statement(self, p):
        return p.declaration_list_opt

    @_("expression ';'")
    def expression_statement(self, p):
        return p.expression

    @_("equality_expression")
    def expression(self, p):
        return p.equality_expression

    @_("equality_expression '=' expression",
       "equality_expression SUBEQ expression",
       "equality_expression ADDEQ expression",
       "equality_expression MULEQ expression",
       "equality_expression MODEQ expression",
       "equality_expression DIVEQ expression")
    def expression(self, p):
        return Binary(p[1], p.equality_expression, p.expression)

    @_("relational_expression")
    def equality_expression(self, p):
        return p.relational_expression

    @_("equality_expression EQ relational_expression",
       "equality_expression NE relational_expression")
    def equality_expression(self, p):
        return Binary(p[1], p.equality_expression, p.relational_expression)

    @_("additive_expression")
    def relational_expression(self, p):
        return p.additive_expression

    @_("relational_expression '<' additive_expression",
       "relational_expression LE  additive_expression",
       "relational_expression '>' additive_expression",
       "relational_expression GE  additive_expression",
       "relational_expression LAND  additive_expression",
       "relational_expression LOR  additive_expression")
    def relational_expression(self, p):
        return Binary(p[1], p.relational_expression, p.additive_expression)

    @_("primary_expression")
    def postfix_expression(self, p):
        return p.primary_expression

    @_("postfix_expression '(' argument_expression_list ')'")
    def postfix_expression(self, p):
        return PostfixExpression(p.postfix_expression, p.argument_expression_list)

    @_("postfix_expression '(' ')'")
    def postfix_expression(self, p):
        return p.postfix_expression

    @_("postfix_expression '[' expression ']'")
    def postfix_expression(self, p):
        return PostfixExpressionArray(p.postfix_expression, p.expression)

    @_("expression")
    def argument_expression_list(self, p):
        return [p.expression]

    @_("argument_expression_list ',' expression")
    def argument_expression_list(self, p):
        return p.argument_expression_list + [p.expression]

    @_("postfix_expression")
    def unary_expression(self, p):
        return p.postfix_expression

    @_("'-' unary_expression")
    def unary_expression(self, p):
        return Unary(p[0], p.unary_expression)

    @_("'+' unary_expression")
    def unary_expression(self, p):
        return Unary(p[0], p.unary_expression)

    @_("'!' unary_expression")
    def unary_expression(self, p):
        return Unary(p[0], p.unary_expression)

    @_("'*' unary_expression")
    def unary_expression(self, p):
        return Unary(p[0], p.unary_expression)

    @_("'&' unary_expression")
    def unary_expression(self, p):
        return Unary(p[0], p.unary_expression)

    @_("unary_expression")
    def mult_expression(self, p):
        return p.unary_expression

    @_("mult_expression '*' unary_expression",
       "mult_expression '/' unary_expression",
       "mult_expression '%' unary_expression")
    def mult_expression(self, p):
        return Binary(p[1], p.mult_expression, p.unary_expression)

    @_("mult_expression")
    def additive_expression(self, p):
        return p.mult_expression

    @_("additive_expression '+' mult_expression",
       "additive_expression '-' mult_expression")
    def additive_expression(self, p):
        return Binary(p[1], p.additive_expression, p.mult_expression)

    @_("ID")
    def primary_expression(self, p):
        return Variable(p[0])

    @_("FNUMBER")
    def primary_expression(self, p):
        return Fnumber(p[0])

    @_("INUMBER")
    def primary_expression(self, p):
        return Inumber(p[0])

    @_("CHARACTER")
    def primary_expression(self, p):
        return Chracter(p[0])

    @_("string_literal")
    def primary_expression(self, p):
        return StringLiteral(p[0])

    @_("'(' expression ')'")
    def primary_expression(self, p):
        return p[1]

    @_("STRING")
    def string_literal(self, p):
        return p[0]

    @_("string_literal STRING")
    def string_literal(self, p):
        return p.string_literal + p[1]
# --------------------------------------------------------------------

    @_("matched",
       "unmatched")
    def statement(self, p):
        return p[0]

    @_("compound_statement",
       "expression_statement",
       "jumstatement")
    def simple_statement(self, p):
        return p[0]
# --------------------------------------------------------------------

    @_("RETURN ';'")
    def jumstatement(self, p):
        return Return(p.empty)

    @_("RETURN expression ';'")
    def jumstatement(self, p):
        return Return(p.expression)

    @_("BREAK ';'")
    def jumstatement(self, p):
        return Break()

    @_("CONTINUE ';'")
    def jumstatement(self, p):
        return Continue()

# --------------------------------------------------------------------
    @_("IF '(' expression ')' statement")
    def unmatched_if(self, p):
        return IfStatement(p.expression, p.statement)

    @_("IF '(' expression ')' matched ELSE unmatched")
    def unmatched_if(self, p):
        return IfStatementElseStatement(p.expression, p.matched, p.unmatched)

    @_("IF '(' expression ')' matched ELSE matched")
    def matched_if(self, p):
        return IfStatementElseStatement(p.expression, p.matched0, p.matched1)

    @_("WHILE '(' expression ')' unmatched")
    def unmatched_while(self, p):
        return WhileLoop(p.expression, p.unmatched)

    @_("WHILE '(' expression ')' matched")
    def matched_while(self, p):
        return WhileLoop(p.expression, p.matched)

    @_("FOR '(' expression_statement expression_statement expression ')' unmatched")
    def unmatched_for(self, p):
        return ForLoop(p.expression_statement0, p.expression_statement1, p.expression, p.unmatched)

    @_("FOR '(' expression_statement expression_statement expression ')' matched")
    def matched_for(self, p):
        return ForLoop(p.expression_statement0, p.expression_statement1, p.expression, p.matched)

    @_("matched_if",
       "matched_while",
       "matched_for",
       "simple_statement")
    def matched(self, p):
        return p[0]

    @_("unmatched_if",
       "unmatched_while",
       "unmatched_for")
    def unmatched(self, p):
        return p[0]
# --------------------------------------------------------------------

    @_("statement")
    def statement_list(self, p):
        return [p.statement]

    @_("statement_list statement")
    def statement_list(self, p):
        return p.statement_list + [p.statement]

    @_("")
    def empty(self, p):
        pass

    def error(self, p):
        
        lineno = p.lineno if p else 'EOF'
        value = p.value if p else 'EOF'
        print(f"{lineno}: Error de Sintaxis en {value}")

        raise SyntaxError()

# _______________________________________________


class RenderAST(Visitor):

    node_default = {
        'shape': 'box',
        'color': 'black',
        'style': 'filled, striped',
        'fillcolor': 'none',
    }
    edge_default = {
        'arrowhead': 'none'

    }

    def __init__(self):
        self.dot = gpv.Digraph(
            'AST', comment='')
        self.dot.attr(
            label=r'\n\nArbol de Sintaxis\n')
        self.dot.attr('node', **self.node_default)
        self.dot.attr('edge', **self.edge_default)
        self.seq = 0

    def name(self):
        self.seq += 1
        return f'n{self.seq:02d}'

    @classmethod
    def render(cls, n: Node):
        dot = cls()
        n.accept(dot)
        return dot.dot

    def visit(self, n: Binary):
        name = self.name()
        self.dot.edge(name, n.left.accept(self))
        self.dot.edge(name, n.right.accept(self))
        return name

    def visit(self, n: Unary):
        name = self.name()
        self.dot.node(name, label=f"Unary\\nop='{n.op}'")
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n: Variable):
        name = self.name()
        self.dot.node(name, label=f"Variable\\n'{n.name}'")
        return name

    def visit(self, n: Inumber):
        name = self.name()
        self.dot.node(name, label=f"Int\\n'{n.name}'")
        return name

    def visit(self, n: Fnumber):
        name = self.name()
        self.dot.node(name, label=f"Float\\n'{n.name}'")
        return name

    def visit(self, n: Chracter):
        name = self.name()
        self.dot.node(name, label=f"Character\\n'{n.name}'")
        return name

    def visit(self, n: StringLiteral):
        name = self.name()
        self.dot.node(name, label=f"String\\n'{n.name}'")
        return name

    def visit(self, n: Ellipsis):
        name = self.name()
        self.dot.node(name, label=f"Ellipsis")
        return name

    def visit(self, n: Return):
        name = self.name()
        self.dot.node(name, label=f"Return")
        self.dot.edge(name, n.expr.accept(self), label="Expression")
        return name

    def visit(self, n: Break):
        name = self.name()
        self.dot.node(name, label=f"Break")
        return name

    def visit(self, n: Continue):
        name = self.name()
        self.dot.node(name, label=f"Continue")
        return name

    def visit(self, n: TranslationUnit):
        name = self.name()
        self.dot.node(name, label=f"Translation Unit")
        for i in range(0, len(n.decl)):
            self.dot.edge(name, n.decl[i].accept(self))
        return name

    def visit(self, n: FuncDefinition):
        name = self.name()
        self.dot.node(
            name, label=f"FuncDefinition\ntype='{n.type}', name='{n.name.name}', static={str(n.static)}")
        if(type(n.stmts) != list):
            n.stmts = [n.stmts]
        for i in range(0, len(n.params)):
            self.dot.edge(name, n.params[i].accept(self), label='Params')

        if n.stmts != None:
            for i in range(0, len(n.stmts)):
                if type(n.stmts[i]) == list:
                    for j in range(0, len(n.stmts[i])):
                        if type(n.stmts[i][j]) != list:
                            self.dot.edge(name, n.stmts[i][j].accept(
                                self), label='Stmts')
                        else:
                            for k in range(0, len(n.stmts[i][j])):
                                self.dot.edge(name, n.stmts[i][j][k].accept(
                                    self), label='Stmts')
                elif n.stmts[i] != None:
                    self.dot.edge(name, n.stmts[i].accept(self), label='Stmts')
        return name

    def visit(self, n: FuncNoParamsDefinition):
        name = self.name()
        self.dot.node(
            name, label=f"FuncNoParamsDefinition\\ntype='{n.type}', name='{n.name.name}', static={str(n.static)}")
        if(type(n.stmts) != list):
            n.stmts = [n.stmts]
        if n.stmts != None:
            for i in range(0, len(n.stmts)):
                if type(n.stmts[i]) == list:
                    for j in range(0, len(n.stmts[i])):
                        self.dot.edge(name, n.stmts[i][j].accept(
                            self), label='Stmts')
                elif n.stmts[i] != None:
                    self.dot.edge(name, n.stmts[i].accept(self), label='Stmts')
        return name

    def visit(self, n: TypeDefinition):
        name = self.name()
        self.dot.node(
            name, label=f"TypeDefinition\\ntype='{n.type}', name='{n.name.name}', const={str(n.Const)}, extern={str(n.Extern)}")
        return name

    def visit(self, n: ExternTypeParams):
        name = self.name()
        self.dot.node(
            name, label=f"ExternTypeParams\\ntype='{n.type}', name='{n.name.name}', const={str(n.Const)}")
        for i in range(0, len(n.params)):
            self.dot.edge(name, n.params[i].accept(self))
        return name

    def visit(self, n: PostfixExpression):
        name = self.name()
        self.dot.node(name, label=f"Postfix Expression\\nname='{n.name.name}'")
        for i in range(0, len(n.argmt)):
            self.dot.edge(name, n.argmt[i].accept(self), label='Argmts')
        return name

    def visit(self, n: PostfixExpressionArray):
        name = self.name()
        self.dot.node(
            name, label=f"Postfix Expression Array\\nname='{n.name.name}'")
        self.dot.edge(name, n.expr.accept(self), label='Argmts')
        return name

    def visit(self, n: IfStatement):
        name = self.name()
        self.dot.node(name, label=f"IfStatement")
        self.dot.edge(name, n.expr.accept(self), label='Expression')
        if(type(n.stmts) != list):
            n.stmts = [n.stmts]
        if n.stmts != None:
            for i in range(0, len(n.stmts)):
                if type(n.stmts[i]) == list:
                    for j in range(0, len(n.stmts[i])):
                        if type(n.stmts[i][j]) != list:
                            self.dot.edge(name, n.stmts[i][j].accept(
                                self), label='Stmts')
                        else:
                            for k in range(0, len(n.stmts[i][j])):
                                self.dot.edge(name, n.stmts[i][j][k].accept(
                                    self), label='Stmts')
                elif n.stmts[i] != None:
                    self.dot.edge(name, n.stmts[i].accept(self), label='Stmts')
        return name

    def visit(self, n: IfStatementElseStatement):
        name = self.name()
        self.dot.node(name, label=f"IfStatementElseStatement")
        self.dot.edge(name, n.expr.accept(self), label='Expression')

        if(type(n.stmts1) != list):
            n.stmts1 = [n.stmts1]

        if(type(n.stmts2) != list):
            n.stmts2 = [n.stmts2]
        if n.stmts1 != None:
            for i in range(0, len(n.stmts1)):
                if type(n.stmts1[i]) == list:
                    for j in range(0, len(n.stmts1[i])):
                        self.dot.edge(name, n.stmts1[i][j].accept(
                            self), label='Ifstmts')
                elif n.stmts1[i] != None:
                    self.dot.edge(name, n.stmts1[i].accept(
                        self), label='Ifstmts')
        if n.stmts2 != None:
            for i in range(0, len(n.stmts2)):
                if type(n.stmts2[i]) == list:
                    for j in range(0, len(n.stmts2[i])):
                        self.dot.edge(name, n.stmts2[i][j].accept(
                            self), label='ElseStmts')
                elif n.stmts2[i] != None:
                    self.dot.edge(name, n.stmts2[i].accept(
                        self), label='ElseStmts')
        return name

    def visit(self, n: WhileLoop):
        name = self.name()
        self.dot.node(name, label=f"WhileLoop")
        self.dot.edge(name, n.expr.accept(self), label='Expression')

        if(type(n.stmts) != list):
            n.stmts = [n.stmts]
        if n.stmts != None:
            for i in range(0, len(n.stmts)):
                if type(n.stmts[i]) == list:
                    for j in range(0, len(n.stmts[i])):
                        self.dot.edge(name, n.stmts[i][j].accept(
                            self), label='Stmts')
                elif n.stmts[i] != None:
                    self.dot.edge(name, n.stmts[i].accept(self), label='Stmts')
        return name

    def visit(self, n: ForLoop):
        name = self.name()
        self.dot.node(name, label=f"ForLoop")
        self.dot.edge(name, n.begin.accept(self), label="Begin")
        self.dot.edge(name, n.expr.accept(self), label="Expr")
        self.dot.edge(name, n.end.accept(self), label="End")
        if(type(n.stmts) != list):
            n.stmts = [n.stmts]
        if n.stmts != None:
            for i in range(0, len(n.stmts)):
                if type(n.stmts[i]) == list:
                    for j in range(0, len(n.stmts[i])):
                        self.dot.edge(name, n.stmts[i][j].accept(
                            self), label='Stmts')
                elif n.stmts[i] != None:
                    self.dot.edge(name, n.stmts[i].accept(self), label='Stmts')
        return name

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} fname")
        exit(1)
    
    l = MyLexer()
    p = Parser()
    txt = open(sys.argv[1], encoding='utf-8').read()

    ast = p.parse(l.tokenize(txt))
    dot = RenderAST.render(ast)

    print(dot)
    #print(ast)

    #dot.save("grafo.dot")
