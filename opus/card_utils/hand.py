from __future__ import annotations

import itertools
import random

from typing import Tuple, Callable, Iterator, TypeVar

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


class Hand:
    def __init__(self, card_string):

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

    def __str__(self):
        return f"♠{self.clubs} ♥{self.hearts} ♦{self.diamonds} ♣{self.clubs}"

    def total_hcp(self):
        return self.spades_points + self.hearts_points + self.diamonds_points + self.clubs_points


def pure_random_deal():
    order = [0] * 13 + [1] * 13 + [2] * 13 + [3] * 13
    random.shuffle(order)

    hands_chars = [["S"], ["S"], ["S"], ["S"]]
    index = 0

    cards = "AKQJT98765432"
    for _ in range(13):
        player = order[index]
        card = cards[index % 13]
        hands_chars[player].append(card)
        index += 1

    for hand_c in hands_chars:
        hand_c.append("H")

    for _ in range(13):
        player = order[index]
        card = cards[index % 13]
        hands_chars[player].append(card)
        index += 1

    for hand_c in hands_chars:
        hand_c.append("D")

    for _ in range(13):
        player = order[index]
        card = cards[index % 13]
        hands_chars[player].append(card)
        index += 1

    for hand_c in hands_chars:
        hand_c.append("C")

    for _ in range(13):
        player = order[index]
        card = cards[index % 13]
        hands_chars[player].append(card)
        index += 1

    return [Hand("".join(c_list)) for c_list in hands_chars]


def generate_rejection_sampled(predicate: Callable[[Hand, Hand], bool]) -> Iterator[Tuple[Hand, Hand]]:
    while True:
        deal = pure_random_deal()
        for pair in itertools.combinations(deal, 2):
            if predicate(*pair):
                yield pair


def generate_type(deal_type: str) -> Iterator[Tuple[Hand, Hand]]:
    deal_type_hcp = {
        "random": 0,
        "game": 24,
        "minor_game": 27,
        "slam": 32
    }
    if deal_type not in deal_type_hcp:
        raise ValueError("deal_type should be one of: " + ", ".join(deal_type_hcp.keys()))

    def pred(h1: Hand, h2: Hand) -> bool:
        return h1.total_hcp() + h2.total_hcp() >= deal_type_hcp[deal_type]

    return generate_rejection_sampled(pred)


T = TypeVar('T')
def take(iterable: Iterator[T], n: int) -> Iterator[T]:
    for _, el in zip(range(n), iterable):
        yield el


def exhaust(iterable: Iterator):
    for _ in iterable:
        pass


if __name__ == '__main__':

    def game_hcp(h1: Hand, h2: Hand) -> bool:
        return h1.total_hcp() + h2.total_hcp() >= 36

    gen_slam = generate_rejection_sampled(game_hcp)
    import time
    t1 = time.time()
    exhaust(take(gen_slam, 1000))
    t2 = time.time()
    print(t2 - t1)



