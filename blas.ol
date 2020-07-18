
not $vulnerable:

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

            H >= 6 and (H + @points >= 14 or AK in H or AQJ in H) and @points <= 10:
                bid 4C

            S >= 6 and (S + @points >= 14 or AK in H or AQJ in H) and @points <= 10:
                bid 4D

            H >= 5:
                bid 2D

            S >= 5:
                bid 2H

            C >= 6 and 2 * C + 0.5 * Cpoints + @points >= 29.5 and @points < 15:
                bid 4H

            D >= 6 and 2 * D + 0.5 * Dpoints + @points >= 29.5 and @points < 15:
                bid 4S

            D >= 5 and  C >= 5:
                bid 2NT

            @points == 8 or @points == 9 or C >= 6:
                bid 2C

            D >= 6:
                bid 3D

            $counts == 5431 and H == 1 and S == 3 and @points >= 10:
                bid 3H

            $counts == 5431 and H == 3 and S == 1 and @points >= 10:
                bid 3S

            H == 3 or S == 3 and @points >= 10 and $balance == 0:
                bid 3D

            @points >= 10 and @points <= 15:
                bid 3NT

            @points == 16 or @points == 17:
                bid 4NT

            @points == 18:
                bid 6NT

            @points == 19 or @points == 20:
                bid 5NT

            2 == 2:
                pass

        @points < 12:
            pass

        @points == 20 or @points == 21:
            bid 2NT

            C >= 5 and H >= 5 and @points >= 7:
                bid 3S

            C >= 6 and 2 * C + 0.5 * Cpoints + @points >= 24.5:
                bid 4H

            D >= 6 and 2 * D + 0.5 * Dpoints + @points >= 24.5:
                bid 4S

        @points >= 12 and @points <= 14:
            bid 1C

        H == 5: bid 1H

        S == 5: bid 1S

        2 == 2: bid 1C

    @points <= 9 and @points >= 5:

        S >= 4 and H >= 4:
            bid 2C

        H == 5 and (C >= 4 or D >= 4):
            bid 2H

        S == 5 and (C >= 4 or D >= 4):
            bid 2S

        S == 6 or H == 6:
            bid 2D

        S == 7:
            bid 3S

        S > 7:
            bid 4S

        H == 7:
            bid 3H

        H > 7:
            bid 4H

        D == 7:
            bid 3D

        D > 7:
            bid 4D

        C == 7:
            bid 3C

        C > 7:
            bid 4C

    @points == 10 or @points == 11:

        S > 5:
            bid 1S

        H > 5:
            bid 1H

    @points >= 12:

        S >= 5:
            bid 1S

        H >= 5:
            bid 1H

        D >= 5:
            bid 1D

        C >= 5:
            bid 1C

        $balance == 4441 and D != 1:
            bid 1C

        2 == 2:
            bid 1C
    2 == 2:
        pass




