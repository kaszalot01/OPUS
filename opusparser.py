from lark import Lark
from lark.indenter import Indenter

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

parser = Lark.open("opuslang.lark", parser='lalr', debug=True, postlex=TreeIndenter())
# AK in ♦:

test_tree = """
D == 2:
    pass
    
S == 2:
    bid 2S

"""

atom_test = " X 5 * Cpoints"

def test():
    print(parser.parse(test_tree).pretty())
    print(parser.parse(test_tree))

if __name__ == '__main__':
    test()


