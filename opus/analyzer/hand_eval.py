from __future__ import annotations
from dataclasses import dataclass, field

from typing import Optional, Iterator

from opus.card_utils import Hand


@dataclass
class Env:
    hand: Hand
    vars: dict = field(default_factory=dict)
    counts: dict = field(default_factory=dict)
    cards: dict = field(default_factory=dict)
    points: dict = field(default_factory=dict)

    @classmethod
    def from_hand(cls, hand: Hand, analyzers: Optional[Iterator[HandAnalyzer]] = None) -> Env:

        env = cls(hand)

        env.points = {
            "C": hand.clubs_points,
            "D": hand.diamonds_points,
            "H": hand.hearts_points,
            "S": hand.spades_points,
            "@": hand.spades_points + hand.hearts_points + hand.diamonds_points + hand.clubs_points
        }
        env.counts = {
            "C": hand.clubs_count,
            "D": hand.diamonds_count,
            "H": hand.hearts_count,
            "S": hand.spades_count,
        }

        env.cards = {
            "C": hand.clubs,
            "D": hand.diamonds,
            "H": hand.hearts,
            "S": hand.spades,
        }

        if analyzers is not None:
            for a in analyzers:
                env.apply_analyzer(a)

        return env

    def apply_analyzer(self, analyzer: HandAnalyzer):
        self.vars.update(analyzer.analyze(self.hand))


class HandAnalyzer:

    def analyze(self, hand: Hand) -> dict:
        return {}


class BalanceAnalyzer(HandAnalyzer):

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


class DummyDictAnalyzer(HandAnalyzer):

    def __init__(self, var_dict: dict):
        self.dict = var_dict

    def analyze(self, hand: Hand) -> dict:
        return self.dict

