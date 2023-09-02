import logging
import sly


from mclexer import MegaLexer


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
    @_("INUMBER")
    def primary_expression(self, p):
        return Inumber(p[0])
    
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
    def visit(self, n: Inumber):
        name = self.name()
        self.dot.node(name, label=f"Int\\n'{n.name}'")
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