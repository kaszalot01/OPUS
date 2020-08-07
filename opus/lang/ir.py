from __future__ import annotations

import lark

from opus.analyzer.hand_eval import Env
from opus.lang.exceptions import UnexpectedToken
from opus.lang.parser import parser
from typing import List, Union, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from lark import Transformer, v_args
from functools import partial, total_ordering
from opus.card_utils.hand import Hand
from itertools import chain


def one_shot_gen(*args):
    for i in args:
        yield i


@total_ordering
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

    cmp_value = {
        "C": 1,
        "D": 2,
        "H": 3,
        "S": 4,
        "NT": 5,
    }

    def __init__(self, meta, symbol):
        self.meta = meta
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

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __lt__(self, other):
        assert isinstance(other, Suit)
        if self.symbol == "@":
            raise ValueError("@ is not comparable")
        return self.cmp_value[self.symbol] < self.cmp_value[other.symbol]


@dataclass
class Branch:
    meta: Optional[Any]
    test: Test
    bids: List[BidStatement]
    children: List[Branch]
    end: Optional[EndStatement] = None

    def children_iterator(self):
        return chain(
            self.test.children_iterator(),
            *[b.children_iterator() for b in self.bids],
            *[b.children_iterator() for b in self.children])

    def __eq__(self, other: Branch):
        return (self.test, self.bids, self.children) == (other.test, other.bids, other.children)


@dataclass
class System:
    branches: List[Branch]

    @classmethod
    def parse_system(cls, opuslang_str):
        try:
            tree = parser.parse(opuslang_str)
        except lark.UnexpectedToken as e:
            raise UnexpectedToken.from_lark(e)

        post_proc = IntermediateTransformer().transform(tree)
        if not hasattr(post_proc, "__iter__"):
            post_proc = [post_proc]
        return cls(post_proc)

    @classmethod
    def load(cls, fname):
        with open(fname) as file:
            return cls.parse_system(file.read())


@dataclass(frozen=True, order=True)
class BidStatement:
    meta: Optional[Any] = field(default=None, compare=False, repr=False)
    level: Optional[int] = 0
    suit: Optional[Suit] = None

    def __post_init__(self):
        if self.level is not None:
            object.__setattr__(self, "level", int(self.level))

    def __str__(self):
        if self.level == 0 and self.suit is None:
            return "pass"
        return f"{self.level}{self.suit}"

    def children_iterator(self):
        return one_shot_gen(self)

    @classmethod
    def from_string(cls, s: str) -> BidStatement:
        if s == "pass":
            return cls(None, None, None)
        num = int(s[0])
        suit = s[1:]
        return BidStatement(None, num, Suit(None, suit))

    @classmethod
    def from_string_seq(cls, s: str) -> Tuple[BidStatement, ...]:
        s = s.replace(" ", "")
        l = s.split("-")
        return tuple(map(BidStatement.from_string, l))


@dataclass(frozen=True)
class EndStatement:
    meta: Optional[lark.Meta] = field(default=None, repr=False)
    label: Optional[str] = None


class ExprType(Enum):
    BOOL = auto()
    NUM = auto()


@dataclass
class InExpr:
    meta: Optional[Any]
    element: Union[InExpr, BinaryExpr, Atom]
    container: Atom

    def eval(self, env):
        assert self.container.type == AtomType.SUIT_CARDS
        element_val = self.element.eval(env)
        container_eval = env.cards[self.container.child.ugly_repr()]
        return set(element_val).issubset(set(container_eval))

    def children_iterator(self):
        return chain(self.element.children_iterator(), self.container.children_iterator())

    def __eq__(self, other: InExpr):
        return (self.element, self.container) == (other.element, other.container)


@dataclass
class BinaryExpr:
    meta: Optional[Any]
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

    def __eq__(self, other):
        return (self.lhs, self.op, self.rhs) == (other.lhs, other.op, other.rhs)


class AtomType(Enum):
    LITERAL       = 1
    SUIT_CARDS    = 2
    SUIT_POINTS   = 3
    VAR           = 4
    NEG           = 5
    CARD_LIST     = 6
    LOGIC_NEG     = 7
    BOOL_LITERAL  = 8

    TYPE_DICT = {
            "num": 1,
            "suit_cards": 2,
            "suit_points": 3,
            "var": 4, 
            "neg": 5,
            "card_list": 6,
    }


class Atom:
    def __init__(self, atom_type, meta, child):
        self.meta = meta
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

        elif self.type is AtomType.BOOL_LITERAL:
            return self.child

    def __repr__(self):
        return f"Atom(atom_type={self.type}, child={self.child})"

    def __eq__(self, other):
        return (self.type, self.child) == (other.type, other.child)

    def children_iterator(self):
        return one_shot_gen(self)


Test = Union[InExpr, BinaryExpr, Atom]


def binary_arithmetic(op, meta, lhs, rhs):
    return BinaryExpr(meta, lhs, op, rhs)


@v_args(inline=True, meta=True)
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

    else_clause = partial(Atom, "BOOL_LITERAL", child=False)

    def start(self, _meta, *children):
        return children

    def branch(self, meta, test, bids_and_branches):
        """bids_and_branches comes from transformation of body rule
        First item will be a list of statements
        second item will either be a list of child branches, or an end statement"""
        if isinstance(bids_and_branches[1], list):
            return Branch(meta, test, bids_and_branches[0], bids_and_branches[1])
        elif isinstance(bids_and_branches[1], EndStatement):
            return Branch(meta, test, bids_and_branches[0], [], bids_and_branches[1])
        else:
            raise ValueError("branch transformer got invalid type in bids_and_branches: {}".format(
                str(type(bids_and_branches[1])))
            )

    def body(self, _meta, *children):
        bids = []
        branches = []
        for c in children:
            if isinstance(c, BidStatement):
                bids.append(c)
            else:
                branches.append(c)
        return bids, branches

    single_bid = body
    branched_bid = body

    def ended_bid(self, _meta, *children):
        bids = []
        end = None
        for i, c in enumerate(children):
            if isinstance(c, BidStatement):
                bids.append(c)
            elif isinstance(c, EndStatement):
                end = c
                if i != len(children) - 1:
                    raise Exception("End should be the end of the branch")

        return bids, end

    end_stmt = EndStatement

    def end_label(self, _meta, child=""):
        return str(child)

    def logic_test(self, meta, lhs, op, rhs):
        return BinaryExpr(meta, lhs, op, rhs)

    add = partial(binary_arithmetic, "+")
    sub = partial(binary_arithmetic, "-")
    mul = partial(binary_arithmetic, "*")
    div = partial(binary_arithmetic, "/")


    cmp_test = logic_test
    in_test = InExpr
    cmp_op = lambda _1, _2, s: str(s)
    logic_op = lambda _1, _2, s: str(s)


test_system = """
AT in S:
    S >= 5:
        pass

    
            
@points >= 20:
    bid 7NT
"""

if __name__ == '__main__':
    system = System.load("./blas.ol")
    h0 = Hand("SAT567HKQD432CA43", analyzers=[BalanceAnalyzer])
    print(h0.env.points["@"])
    print(h0.env.vars['balance'])
    h1 = Hand("SQJ8HAT89DAK8CAJ2", analyzers=[BalanceAnalyzer])
    print(h1.env.points["@"])
    ex = Executor(system, h0, h1)
    ex.execute(system.branches)
    print(ex.result)
