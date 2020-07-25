from lark import Lark
from opus.lang.parser import parser
import pytest


def test_basic_grammar():
    test_tree = \
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
"""
    _ = parser.parse(test_tree)

def test_contains_operator():
    test_tree = \
"""
@points > 21:
    bid 2♦

    ♥ >= 4 and AK in ♥:
        bid 2♠

"""
    _ = parser.parse(test_tree)

def test_bid_after_branch():
    test_tree = \
"""
@points > 21:
    bid 2♦

    ♥ >= 4 and @points < 15:
        bid 2♠

    bid 2H
    @points >= 15 and @points <= 17 and ♠ >= 2 and ♥ >= 2:
        bid 4♣

"""
    with pytest.raises(Exception):
        _ = parser.parse(test_tree)


def test_comments():
    test_tree = \
"""
# top level
@points > 21:
    bid 2♦
    # correctly indented

    ♥ >= 4 and AK in ♥:
        bid 2♠

"""
    _ = parser.parse(test_tree)
