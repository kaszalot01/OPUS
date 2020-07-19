from __future__ import annotations
from dataclasses import dataclass, field

from typing import Tuple

POINT_DICT = {
    "A": 4,
    "K": 3,
    "Q": 2,
    "J": 1,
    "T": 0,
    "9": 0,
    "8": 0,
    "7": 0,
    "6": 0,
    "5": 0,
    "4": 0,
    "3": 0,
    "2": 0,
}


def split_by_predicate(s, predicate):
    if predicate(s[0]):
        s = s[1:]
    current = ""
    result = []
    for c in s:
        if predicate(c):
            result.append(current)
            current = ""
        else:
            current += c
    result.append(current)
    return result


def count_hcp(suit_string):
    return sum(map(lambda c: POINT_DICT[c], suit_string))


@dataclass
class Env:
    vars: dict = field(default_factory=dict)
    counts: dict = field(default_factory=dict)
    cards: dict = field(default_factory=dict)
    points: dict = field(default_factory=dict)


class HandAnalyzer:

    def analyze(self, hand: Hand):
        return {}


class Hand:
    def __init__(self, card_string, analyzers: Tuple[HandAnalyzer] = ()):

        by_color = split_by_predicate(card_string, lambda c: c in "CDHS")

        self.clubs = by_color[3]
        self.clubs_count = len(by_color[3])
        self.clubs_points = count_hcp(self.clubs)

        self.diamonds = by_color[2]
        self.diamonds_count = len(by_color[2])
        self.diamonds_points = count_hcp(self.diamonds)

        self.hearts = by_color[1]
        self.hearts_count = len(by_color[1])
        self.hearts_points = count_hcp(self.hearts)

        self.spades = by_color[0]
        self.spades_count = len(by_color[0])
        self.spades_points = count_hcp(self.spades)

        self.env = Env()

        for analyzer in analyzers:
            new_vars = analyzer.analyze(self)
            self.env.vars.update(new_vars)

        self.env.points = {
            "C": self.clubs_points,
            "D": self.diamonds_points,
            "H": self.hearts_points,
            "S": self.spades_points,
            "@": self.spades_points + self.hearts_points + self.diamonds_points + self.clubs_points
        }
        self.env.counts = {
            "C": self.clubs_count,
            "D": self.diamonds_count,
            "H": self.hearts_count,
            "S": self.spades_count,
        }

        self.env.cards = {
            "C": self.clubs,
            "D": self.diamonds,
            "H": self.hearts,
            "S": self.spades,
        }

