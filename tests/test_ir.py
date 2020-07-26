from opus.lang.ir import System, Executor, BalanceAnalyzer, SystemIncompleteException
import pathlib
from opus.card_utils.hand import Hand
from lark import Tree


def test_blas_parses():
    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'
    system = System.load(system_fname)

    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)


def test_blas_executes():

    here = pathlib.Path(__file__)
    root = here.parent.parent
    system_fname = root / 'blas.ol'

    system = System.load(system_fname)
    h0 = Hand("SAT567HKQD432CA43", analyzers=(BalanceAnalyzer(),))
    h1 = Hand("SQJ8HAT89DAK8CAJ2", analyzers=(BalanceAnalyzer(),))
    h0.env.vars['vulnerable'] = False
    h1.env.vars['vulnerable'] = False
    ex = Executor(system, h0, h1)
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
