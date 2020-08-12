import pathlib

from opus.analyzer.execute import Executor
from opus.analyzer.hand_eval import BalanceAnalyzer, DummyDictAnalyzer
from opus.card_utils import Hand
from opus.lang.exceptions import SystemIncompleteException
from opus.lang.ir import System, BidStatement


def test_stayman():
    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'

    system = System.load(system_fname)

    h0 = Hand("SAKJ97H983DQJCAQ6")
    h1 = Hand("S2HAJT6D6432CKJT9")

    vulnerable_analyzer = DummyDictAnalyzer({"vulnerable": False})
    ex = Executor(system, h0, h1, [vulnerable_analyzer, BalanceAnalyzer()])
    try:
        ex.execute(system.branches)
    except SystemIncompleteException:
        pass

    res = tuple(ex.result)
    assert res == BidStatement.from_string_seq("1NT-2C-2S-3NT")


WRONG_OPENINGS_DATA = """
♠94 ♥T5 ♦Q7542 ♣AK84
♠76 ♥AKJ732 ♦AK ♣Q73

♠J3 ♥AJT3 ♦2 ♣A86432
♠AKQ74 ♥KQ75 ♦7 ♣J95

♠4 ♥A832 ♦AJ87 ♣QT85
♠AKQ7 ♥KJ ♦K65 ♣AJ62

♠AK875 ♥QJT76 ♦4 ♣53
♠J ♥K94 ♦KQ8765 ♣AK4

♠64 ♥A ♦985 ♣AK98654
♠AQ85 ♥KQJ64 ♦32 ♣J3

♠A43 ♥K ♦T762 ♣KT876
♠JT9 ♥AQ74 ♦A3 ♣AQ52

♠A9643 ♥Q953 ♦A972 ♣
♠T8 ♥A87 ♦Q ♣AKJT653

♠7653 ♥Q ♦KJT976 ♣98
♠AKJ ♥K87 ♦Q54 ♣KQ72

♠ ♥A752 ♦AT7 ♣KT5432
♠A653 ♥KT84 ♦Q ♣AQ97
"""


def test_openings():

    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'

    vulnerable_analyzer = DummyDictAnalyzer({"vulnerable": False})

    system = System.load(system_fname)
    cases = map(lambda rows: rows.strip().split("\n"), WRONG_OPENINGS_DATA.split("\n\n"))
    for h0_str, h1_str in cases:
        ex = Executor(system, Hand(h0_str), Hand(h1_str), [vulnerable_analyzer, BalanceAnalyzer()])

        try:
            ex.execute(system.branches)
        except SystemIncompleteException:
            pass

        print(h0_str)
        print(h1_str)
        print()

        assert len(ex.result) != 0
