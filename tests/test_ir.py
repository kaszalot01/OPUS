import pytest

from opus.lang.ir import System, Suit, BidStatement
from opus.analyzer.execute import Executor
from opus.analyzer.hand_eval import BalanceAnalyzer, HandAnalyzer, DummyDictAnalyzer
from opus.lang.exceptions import SystemIncompleteException
import pathlib
from opus.card_utils.hand import Hand
from lark import Tree, Token


def test_blas_parses():
    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'
    system = System.load(system_fname)

    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)


def test_simple_ir_parse():
    test_system = \
"""
@points > 21:
    bid 2♦

    ♥ >= 4 and @points < 15:
        bid 2♠
    @points >= 15 and @points <= 17 and ♠ >= 2 and ♥ >= 2:
        pass

    $balance == 1 or $balance == 2:
        @points >= 15 and @points <= 17:
            bid 1NT

            ((♥ == 4 or ♠ == 4) and @points >= 8) or (♥ >=4 and ♠ >= 4):
                bid 2♣

            ♣ >- 6 and 2 * ♣ + 0.5 * ♣points + @points >= 29.5 and @points < 15:
                bid 4♥
    else:
        pass
"""
    system = System.parse_system(test_system)
    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)
            assert not isinstance(c, Token)


def test_blas_executes():

    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'

    system = System.load(system_fname)
    h0 = Hand("SAT567HKQD432CA43")
    h1 = Hand("SQJ8HAT89DAK8CAJ2")
    vulnerable_analyzer = DummyDictAnalyzer({"vulnerable": False})
    ex = Executor(system, h0, h1, [vulnerable_analyzer, BalanceAnalyzer()])
    try:
        ex.execute(system.branches)
    except SystemIncompleteException:
        pass


def test_ir_equality():
    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'

    system1 = System.load(system_fname)
    system2 = System.load(system_fname)

    assert system1 == system2


def test_comments():
    without_comment = \
"""
@points > 21:
    bid 2♦
    ♥ >= 4 and AK in ♥:
        bid 2♠

"""

    with_comment = \
"""
# top level
@points > 21:
    bid 2♦
    # correctly indented

    ♥ >= 4 and AK in ♥:
        bid 2♠

"""
    s_comment = System.parse_system(with_comment)
    s_no_comment = (System.parse_system(without_comment))
    assert s_comment == s_no_comment


def test_suit_cmp():
    assert Suit(None, 'NT') > Suit(None, 'C')
    assert Suit(None, 'NT') > Suit(None, 'D')
    assert Suit(None, 'NT') > Suit(None, 'S')
    assert Suit(None, 'S') > Suit(None, 'H')
    assert Suit(None, 'S') > Suit(None, 'C')
    assert Suit(None, 'H') > Suit(None, 'D')

    with pytest.raises(Exception):
        _ = Suit(None, "@") < Suit(None, "NT")
    with pytest.raises(Exception):
        _ = Suit(None, "@") > Suit(None, "NT")


def test_bid_statement_cmp():
    assert BidStatement(None, 1, Suit(None, "C")) < BidStatement(None, 1, Suit(None, "NT"))
    assert BidStatement(None, 1, Suit(None, "C")) < BidStatement(None, 1, Suit(None, "S"))
    assert BidStatement(None, 4, Suit(None, "C")) > BidStatement(None, 1, Suit(None, "S"))
    assert BidStatement(None, 4, Suit(None, "C")) > BidStatement(None, 3, Suit(None, "NT"))
    assert BidStatement(None, 2, Suit(None, "D")) < BidStatement(None, 2, Suit(None, "H"))


def test_end_statement_usage():
    test_system = \
"""
@points > 21:
    bid 2♦

    ♥ >= 4 and @points < 15:
        bid 2♠
        end  # both blank...

    @points >= 15 and @points <= 17 and ♠ >= 2 and ♥ >= 2:
        bid 4♣
        end gf   # and labeled ends are acceptable
"""
    system = System.parse_system(test_system)

    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)
            assert not isinstance(c, Token)
    pass
