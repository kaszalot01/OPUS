from __future__ import annotations
from collections import Counter, defaultdict

from typing import List, Tuple, DefaultDict, Union

from opus.card_utils import Hand, generate_type, take
from opus.lang.ir import System, BidStatement, Suit
from opus.analyzer.execute import Executor
from opus.analyzer.hand_eval import BalanceAnalyzer, DummyDictAnalyzer
from opus.lang.exceptions import UnexpectedToken, SystemIncompleteException


class BranchReport:

    def __init__(self):
        self.counter: DefaultDict[BidStatement, List[Union[int, BranchReport]]] = defaultdict(lambda: [0, BranchReport()])

    def add(self, bids: Tuple[BidStatement, ...]):

        if len(bids) > 0:
            head, *tail = bids
            self.counter[head][0] += 1
            self.counter[head][1].add(tail)
        else:
            self.counter[()][0] += 1

    def is_leaf(self) -> bool:
        return len(self.counter) == 1 and () in self.counter

    def all_routes(self) -> List[Tuple[int, Tuple[BidStatement]]]:
        if self.is_leaf():
            return [(self.counter[()][0], ())]
        result = []
        for start, (count, rep) in self.counter.items():
            child_routes = rep.all_routes()
            if start == ():
                assert len(child_routes) == 0
                result.append((count, start))
            for route_count, route_bids in child_routes:

                result.append((route_count, (start,) + route_bids))
        result.sort(reverse=True)
        return result

    def starts_with(self, s: str) -> BranchReport:
        num = int(s[0])
        suit_str = s[1:]
        bid_stmt = BidStatement(None, num, Suit(None, suit_str))
        return self.counter[bid_stmt][1]


def repl(rep: BranchReport, root=()):
    while True:
        print("Przeglądasz gałąź:\nStart: ", " - ".join(map(str, root)))

        print("Następne odzywki:")
        for bid, (count, _) in rep.counter.items():
            print(f"{bid}: {count}")

        ans = input("\nPrzeglądaj gałąź ('.' aby wrócić gałąź wyżej): ")
        if ans == ".":
            return
        bid_ans = BidStatement.from_string(ans)
        _, child = rep.counter[bid_ans]
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
            cause = e

        counter[tuple(ex.result)] += 1
        if tuple(ex.result) == BidStatement.from_string_seq("1NT-2C"):
            print("UWAGA TEN DEBIL SPASOWAL NA STAYMANA")
            print("\n".join(map(str, pair)))
            print()

        if len(ex.result) == 0:
            print("UWAGA TEN DEBIL NIC NIE ZROBIL NA OTWARCIU")
            print("\n".join(map(str, pair)))
            print()
        rep.add(ex.result)

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

