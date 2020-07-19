from opus.lang.ir import System, Executor, BalanceAnalyzer, SystemIncompleteException
from opus.card_utils.hand import Hand
from lark import Tree


def test_blas_parses():
    system = System.load('./blas.ol')

    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)


def test_blas_executes():

    system = System.load('./blas.ol')
    h0 = Hand("SAT567HKQD432CA43", analyzers=(BalanceAnalyzer(),))
    h1 = Hand("SQJ8HAT89DAK8CAJ2", analyzers=(BalanceAnalyzer(),))
    h0.env.vars['vulnerable'] = False
    h1.env.vars['vulnerable'] = False
    ex = Executor(system, h0, h1)
    try:
        ex.execute(system.branches)
    except SystemIncompleteException:
        pass
