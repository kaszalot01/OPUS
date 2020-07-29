from typing import List, Optional, Iterator

from opus.analyzer.hand_eval import Env, HandAnalyzer
from opus.card_utils import Hand
from opus.lang.exceptions import SystemIncompleteException
from opus.lang.ir import System, Branch, BidStatement


class Executor:

    def __init__(self, system: System, hand0: Hand, hand1: Hand, analyzers: Optional[Iterator[HandAnalyzer]] = None):
        self.system = system

        self.hand0 = hand0
        self.hand1 = hand1

        self.env0 = Env.from_hand(hand0, analyzers)
        self.env1 = Env.from_hand(hand1, analyzers)

        self.hands = [hand0, hand1]
        self.envs = [self.env0, self.env1]

        self.bidding_hand = 0

        self.result = ""

    def execute(self, branches: List[Branch]):
        for branch in branches:
            test_eval = branch.test.eval(self.envs[self.bidding_hand])
            assert isinstance(test_eval, bool)

            if test_eval:
                for bid in branch.bids:
                    self.bid(bid)
                self.execute(branch.children)
                return
        raise SystemIncompleteException("System incomplete")

    def bid(self, bid_statement: BidStatement):
        self.result += f"{bid_statement} - "
        self.bidding_hand = 1 - self.bidding_hand
