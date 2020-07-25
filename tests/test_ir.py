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
