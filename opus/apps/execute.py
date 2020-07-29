import sys

from opus.card_utils import Hand
from opus.lang.ir import System
from opus.analyzer.execute import Executor
from opus.analyzer.hand_eval import BalanceAnalyzer
from opus.lang.exceptions import UnexpectedToken, SystemIncompleteException


def execute(fname):

    try:
        system = System.load(fname)
    except UnexpectedToken as e:
        print(e, file=sys.stderr)
        exit(1)

    h0 = Hand("SAK6HKQ4DQJ93C952", analyzers=(BalanceAnalyzer(),))
    h1 = Hand("SQ9872HAJ73D93CK2", analyzers=(BalanceAnalyzer(),))

    h0.env.vars["vulnerable"] = False
    h1.env.vars["vulnerable"] = False

    ex = Executor(system, h0, h1)
    try:
        ex.execute(system.branches)
    except SystemIncompleteException as e:
        print(e)
    print(ex.result)

