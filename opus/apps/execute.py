from __future__ import annotations

import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from typing import List, Tuple, DefaultDict, Union, Optional

from opus.card_utils import Hand, generate_type, take
from opus.lang.ir import System, BidStatement, Suit
from opus.analyzer.execute import Executor
from opus.analyzer.hand_eval import BalanceAnalyzer, DummyDictAnalyzer
from opus.lang.exceptions import UnexpectedToken, SystemIncompleteException


PLACEHOLDER_ERROR_BID = BidStatement.from_string("8C")


class BranchReport:

    def __init__(self):
        self.counter: DefaultDict[BidStatement, SubBranch] = defaultdict(SubBranch)

    def add(self, bids: Tuple[BidStatement, ...], deal: Tuple[Hand, Hand]):

        if len(bids) > 0:
            head, *tail = bids
            self.counter[head].count += 1
            self.counter[head].report.add(tail, deal)
            if len(tail) >= 1 and tail[-1] == PLACEHOLDER_ERROR_BID:
                self.counter[head].correct_bidding = False

        else:
            self.counter[()].count += 1
            self.counter[()].leaf = True
            self.counter[()].deals.append(deal)

    def is_leaf(self) -> bool:
        return len(self.counter) == 1 and () in self.counter

    def all_routes(self) -> List[Tuple[int, Tuple[BidStatement]]]:
        if self.is_leaf():
            return [(self.counter[()].count, ())]
        result = []
        for start, sub in self.counter.items():
            rep = sub.report
            count = sub.count
            child_routes = rep.all_routes()
            if start == ():
                assert len(child_routes) == 0
                result.append((count, start))
            for route_count, route_bids in child_routes:

                result.append((route_count, (start,) + route_bids))
        result.sort(reverse=True)
        return result

    def deal_iter(self):
        result = iter(())
        for sub in self.counter.values():
            if sub.leaf:
                result = itertools.chain(result, sub.deals)
            else:
                result = itertools.chain(result, sub.report.deal_iter())

        return result

    def starts_with(self, s: str) -> BranchReport:
        num = int(s[0])
        suit_str = s[1:]
        bid_stmt = BidStatement(None, num, Suit(None, suit_str))
        return self.counter[bid_stmt].report


@dataclass
class SubBranch:
    count: int = 0
    report: BranchReport = field(default_factory=BranchReport)
    correct_bidding: bool = True
    leaf: bool = False
    deals: List[Tuple[Hand, Hand]] = field(default_factory=list)


def repl(rep: BranchReport, root=()):

    def intro_stirng(b: BidStatement, s: SubBranch) -> str:
        correct = "✔"
        incorrect = "✕"
        emoji = correct if s.correct_bidding else incorrect
        return f"{str(b):<3} {emoji} - {s.count}"

    while True:
        print("Przeglądasz gałąź:\nStart: ", " - ".join(map(str, root)))

        print("Następne odzywki:")
        for bid, sub in rep.counter.items():
            print(intro_stirng(bid, sub))

        ans = input("\nPrzeglądaj gałąź ('.' aby wrócić gałąź wyżej): ")
        if ans == ".":
            return
        elif ans == "p":
            l = list(take(rep.deal_iter(), 5))
            for pair in l:
                print(pair[0])
                print(pair[1])
                print()
        else:
            bid_ans = BidStatement.from_string(ans)
            child = rep.counter[bid_ans].report
            repl(child, root + (bid_ans,))


def execute(fname):

    gen = generate_type("game")

    system = System.load("blas.ol")

    counter = Counter()

    rep = BranchReport()

    vulnerable_analyzer = DummyDictAnalyzer({"vulnerable": False})
    balance_analyzer = BalanceAnalyzer()

    for pair in take(gen, 1000):
        ex = Executor(system, pair[0], pair[1], [vulnerable_analyzer, balance_analyzer])

        try:
            ex.execute(system.branches)
        except SystemIncompleteException as e:
            ex.result.append(PLACEHOLDER_ERROR_BID)

        counter[tuple(ex.result)] += 1
        if tuple(ex.result) == BidStatement.from_string_seq("1NT-2C"):
            print("UWAGA TEN DEBIL SPASOWAL NA STAYMANA")
            print("\n".join(map(str, pair)))
            print()

        if len(ex.result) == 0:
            print("UWAGA TEN DEBIL NIC NIE ZROBIL NA OTWARCIU")
            print("\n".join(map(str, pair)))
            print()
        rep.add(ex.result, pair)

    repl(rep)

    print("hejho")
    #
    # rep.add(BidStatement.from_string_seq("1NT - 2C - 2D"))
    # rep.add(BidStatement.from_string_seq("1NT - 2C - 2D"))
    # rep.add(BidStatement.from_string_seq("1NT - 2C - 2H - 2NT - 4H"))
    # rep.add(BidStatement.from_string_seq("1NT - 2C - 2H - 2NT - 4H"))
    # rep.add(BidStatement.from_string_seq("1NT - 2C - 2H - 2NT"))
    # rep.add(BidStatement.from_string_seq("1NT - 2D"))
    #
    # # med = rep.starts_with("1NT")
    # res = rep.all_routes()
    #
    # for count, bids in res:
    #     print(count, " - ".join(map(str, bids)))

