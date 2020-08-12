from lark import Lark, UnexpectedToken
from opus.lang.parser import parser
import pytest
from pathlib import Path


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
    else:
        pass
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

    ♥ >= 4 and AK in ♥:  # inline1
        bid 2♠  # inline2

"""
    _ = parser.parse(test_tree)


def test_no_anonymous_tokens():
    from copy import deepcopy
    import random

    here = Path(__file__)
    blas_fname = here.parent.parent / "blas.ol"
    with open(blas_fname) as file:
        blas_text = file.read()

    blas_lines = blas_text.split("\n")

    for _ in range(100):
        lines_copy = deepcopy(blas_lines)

        victim_index = random.randrange(len(lines_copy))
        victim_list = list(lines_copy[victim_index])
        try:
            insertion_point = random.randrange(len(victim_list))
        except ValueError:
            continue
        victim_list[insertion_point:insertion_point] = list("error_here")
        lines_copy[victim_index] = "".join(victim_list)
        bad_system_text = "\n".join(lines_copy)
        try:
            _ = parser.parse(bad_system_text)
        except UnexpectedToken as e:
            for token_name in e.expected:
                assert "ANON" not in token_name
        except:
            pass


def test_end_statement_usage():
    test_tree = \
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
    _ = parser.parse(test_tree)
