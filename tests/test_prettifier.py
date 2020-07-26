from opus.apps import prettyfier


def test_suits():
    system_text = """

@points > 21:
    bid 2D

    H >=4 and @points < 15:
        bid 2S

    @points >= 15 and  @points <= 17 and S >= 2 and H >= 2:
        bid 4C

"""

    expected = """

@points > 21:
    bid 2♦

    ♥ >=4 and @points < 15:
        bid 2♠

    @points >= 15 and  @points <= 17 and ♠ >= 2 and ♥ >= 2:
        bid 4♣

"""
    prettified = prettyfier.prettify(system_text, True, False)
    assert prettified == expected


def test_player_comments():
    system_text = """

@points > 21:
    bid 2D

    H >=4 and @points < 15:
        bid 2S

    @points >= 15 and  @points <= 17 and S >= 2 and H >= 2:
        bid 4C

$balance == 2 or $balance == 1:

    @points >= 15 and @points <= 17:
        bid 1NT

        ((H == 4 or S == 4) and @points >= 8) or (H >= 4 and S >= 4):
            bid 2C
"""

    expected = """

@points > 21:
    bid 2D  # player 1

    H >=4 and @points < 15:
        bid 2S  # player 2

    @points >= 15 and  @points <= 17 and S >= 2 and H >= 2:
        bid 4C  # player 2

$balance == 2 or $balance == 1:

    @points >= 15 and @points <= 17:
        bid 1NT  # player 1

        ((H == 4 or S == 4) and @points >= 8) or (H >= 4 and S >= 4):
            bid 2C  # player 2
"""
    prettified = prettyfier.prettify(system_text, suits=False, bids=True)
    assert prettified == expected
