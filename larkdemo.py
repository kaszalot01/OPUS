#
# This example demonstrates usage of the Indenter class.
#
# Since indentation is context-sensitive, a postlex stage is introduced to
# manufacture INDENT/DEDENT tokens.
#
# It is crucial for the indenter that the NL_type matches
# the spaces (and tabs) after the newline.
#

from lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL+ stmt+ 

    ?stmt: bid_stmt | branch

    branch: test ":" body
    body: bid_stmt | _NL _INDENT stmt+ _DEDENT

    ?atom: NUMBER               -> number
        | "(" test ")"  
        | "(" sum ")"

    ?val: suit                  -> suit_cards
        | suit "points"         -> suit_points
        | "$" NAME              -> var
        | atom

    ?sum: product
        | sum "+" product
        | sum "-" product

    ?product: val
        | product "*" val      -> mul
        | product "/" val      -> div


    test: cmp_stmt              -> compare
        | "not" test            -> neg
        | test logic_op test    -> logic

    ?cmp_stmt: sum cmp_op sum
    !cmp_op: (">" | ">=" | "==" | "<=" | "<")

    !logic_op: "or" | "and"

    !bid_stmt: "bid" _BID_NUM suit _NL

    !suit: "♣" | "♦" | "♥" | "♠" | "C" | "D" | "H" | "S" | "NT" | "@"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE

    _BID_NUM: /[1-7]/
    _NL: /(\r?\n[\t ]*)+/
"""

# TODO arithmetic and boolean collisions. set up pytest
class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())
# parser = Lark(tree_grammar, postlex=TreeIndenter())

test_tree = """
@points > 21:
    bid 2♦

    ♥ >= 4 and @points < 15:
        bid 2♠
    @points >= 15 and @points <= 17 and ♠ >= 2 and ♥ >= 2:
        bid 4♣

    $balance == 1 or $balance == 2:
        @points >= 15 and @points <= 17:
            bid 1NT

            ((♥ == 4 or ♠ == 4) and @points >= 8) or (♥ >=4 and ♠ >= 4):
                bid 2♣

            ♣ >- 6 and 2 * ♣ + 0.5 * ♣points + @points >= 29.5 and @points < 15:
                bid 4♥
"""

atom_test = " X 5 * Cpoints"

def test():
    print(parser.parse(test_tree).pretty())
    print(parser.parse(test_tree))
    # print(parser.parse(atom_test).pretty())
    # print(parser.parse(atom_test))

if __name__ == '__main__':
    test()


