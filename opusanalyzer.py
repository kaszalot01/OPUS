from __future__ import annotations

from opusparser import parser
from typing import List, Union, Optional
from dataclasses import dataclass
from enum import Enum, auto
from lark import Transformer, v_args
from functools import partial
from opusexecute import Hand, Env
from itertools import chain


def one_shot_gen(*args):
    for i in args:
        yield i

class Suit:
    pretty_to_ugly = {
        "♣": "C",
        "♦": "D",
        "♥": "H",
        "♠": "S",
        "NT": "NT",
        "@": "@"
    }

    ugly_to_pretty = {v: k for k, v in pretty_to_ugly.items()}

    def __init__(self, symbol):
        symbol = str(symbol)  # convert lark Token to str
        if symbol in self.pretty_to_ugly:
            symbol = self.pretty_to_ugly[symbol]
        elif symbol in self.ugly_to_pretty:
            pass
        else:
            raise ValueError(f"Incorrect suit symbol: {symbol}")
        self.symbol = symbol

    def ugly_repr(self):
        return self.symbol

    def __str__(self):
        return self.ugly_to_pretty[self.symbol]

    def __repr__(self):
        return f"Suit('{self.ugly_to_pretty[self.symbol]}')"

    def __hash__(self):
        return hash(str(self))


@dataclass
class Branch:
    test: BinaryExpr
    bids: List[BidStatement]
    children: List[Branch]

    def children_iterator(self):
        return chain(
            self.test.children_iterator(),
            *[b.children_iterator() for b in self.bids],
            *[b.children_iterator() for b in self.children])


@dataclass
class System:
    branches: List[Branch]

    @classmethod
    def parse_system(cls, opuslang_str):
        tree = parser.parse(opuslang_str)
        post_proc = IntermediateTransformer().transform(tree)
        if not isinstance(post_proc, list):
            post_proc = [post_proc]
        return cls(post_proc)

    @classmethod
    def load(cls, fname):
        with open(fname) as file:
            return cls.parse_system(file.read())


@dataclass
class BidStatement:
    level: Optional[int] = None
    suit: Optional[Suit] = None

    def __str__(self):
        if self.level is None and self.suit is None:
            return "pass"
        return f"{self.level}{self.suit}"

    def children_iterator(self):
        return one_shot_gen(self)
    

class ExprType(Enum):
    BOOL = auto()
    NUM = auto()


@dataclass
class InExpr:
    element: Union[InExpr, BinaryExpr, Atom]
    container: Atom

    def eval(self, env):
        assert self.container.type == AtomType.SUIT_CARDS
        element_val = self.element.eval(env)
        container_eval = env.cards[self.container.child.ugly_repr()]
        return set(element_val).issubset(set(container_eval))

    def children_iterator(self):
        return chain(self.element.children_iterator(), self.container.children_iterator())


@dataclass
class BinaryExpr:
    lhs: Union[InExpr, BinaryExpr, Atom]
    op: str
    rhs: Union[InExpr, BinaryExpr, Atom]

    def eval(self, env):
        lhs_val = self.lhs.eval(env)
        rhs_val = self.rhs.eval(env)
        op = str(self.op)
        eval_str = f"{lhs_val} {op} {rhs_val}"
        return eval(eval_str)

    def children_iterator(self):
        return chain(self.lhs.children_iterator(), self.rhs.children_iterator())


class AtomType(Enum):
    LITERAL       = 1
    SUIT_CARDS    = 2
    SUIT_POINTS   = 3
    VAR           = 4
    NEG           = 5
    CARD_LIST     = 6
    LOGIC_NEG     = 7

    TYPE_DICT = {
            "num": 1,
            "suit_cards": 2,
            "suit_points": 3,
            "var": 4, 
            "neg": 5,
            "card_list": 6,
    }


class Atom:
    def __init__(self, atom_type, child):
        self.child = child
        self.type = AtomType[atom_type]

    def eval(self, env: Env):

        if self.type is AtomType.LITERAL:
            return float(self.child)

        elif self.type is AtomType.SUIT_CARDS:
            return env.counts[self.child.ugly_repr()]

        elif self.type is AtomType.SUIT_POINTS:
            return env.points[self.child.ugly_repr()]

        elif self.type is AtomType.VAR:
            return env.vars[str(self.child)]

        elif self.type is AtomType.NEG:
            return -self.child.eval(env)

        elif self.type is AtomType.CARD_LIST:
            return str(self.child)

        elif self.type is AtomType.LOGIC_NEG:
            child_val = self.child.eval(env)
            assert isinstance(child_val, bool)
            return not child_val

    def __repr__(self):
        return f"Atom(atom_type={self.type}, child={self.child})"

    def children_iterator(self):
        return one_shot_gen(self)


def binary_arithmetic(op, lhs, rhs):
    return BinaryExpr(lhs, op, rhs)


@v_args(inline=True)
class IntermediateTransformer(Transformer):

    atom = Atom
    clubs = diamonds = hearts = spades = no_trump = all = Suit
    suit_points = partial(Atom, "SUIT_POINTS")
    suit_cards = partial(Atom, "SUIT_CARDS")
    var = partial(Atom, "VAR")
    neg = partial(Atom, "NEG")
    num = partial(Atom, "LITERAL")
    card_list = partial(Atom, "CARD_LIST")
    logic_neg = partial(Atom, "LOGIC_NEG")

    bid_stmt = BidStatement
    suit = Suit

    def start(self, *children):
        return children

    def branch(self, test, bids_and_branches):
        return Branch(test, bids_and_branches[0], bids_and_branches[1])

    def body(self, *children):
        bids = []
        branches = []
        for c in children:
            if isinstance(c, BidStatement):
                bids.append(c)
            else:
                branches.append(c)
        return bids, branches

    def logic_test(self, lhs, op, rhs):
        return BinaryExpr(lhs, op, rhs)

    add = partial(binary_arithmetic, "+")
    sub = partial(binary_arithmetic, "-")
    mul = partial(binary_arithmetic, "*")
    div = partial(binary_arithmetic, "/")

    cmp_test = logic_test
    in_test = InExpr
    cmp_op = str
    logic_op = str


class SystemIncompleteException(Exception):
    pass

class Executor:

    def __init__(self, system: System, hand0: Hand, hand1: Hand):
        self.system = system
        self.hand0 = hand0
        self.hand1 = hand1
        self.hands = [hand0, hand1]
        self.bidding_hand = 0

        self.result = ""

    def execute(self, branches: List[Branch]):
        for branch in branches:
            test_eval = branch.test.eval(self.hands[self.bidding_hand].env)
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





test_system = """
AT in S:
    S >= 5:
        pass

    
            
@points >= 20:
    bid 7NT
"""


class BalanceAnalyzer:

    @staticmethod
    def analyze(hand: Hand):
        counts = [hand.clubs_count, hand.diamonds_count, hand.hearts_count, hand.spades_count]
        counts.sort(reverse=True)
        if counts[0] == 4 and counts[-1] > 1:
            balance = 2
        elif counts == [5, 3, 3, 2]:
            balance = 1
        else:
            balance = 0
        return {"balance": balance}


if __name__ == '__main__':
    system = System.parse_system(test_system)
    h0 = Hand("SAT567HKQD432CA43", analyzers=[BalanceAnalyzer])
    print(h0.env.points["@"])
    print(h0.env.vars['balance'])
    h1 = Hand("SQJ8HAT89DAK8CAJ2", analyzers=[BalanceAnalyzer])
    print(h1.env.points["@"])
    ex = Executor(system, h0, h1)
    ex.execute(system.branches)
    print(ex.result)
