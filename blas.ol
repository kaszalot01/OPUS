
not $vulnerable:

    # acol
    @points > 21:
        bid 2D

        H >=4 and @points < 15:
            bid 2S

        @points >= 15 and  @points <= 17 and S >= 2 and H >= 2:
            bid 4C

    # sklad zrownowazony
    $balance == 2 or $balance == 1:

        @points >= 15 and @points <= 17:
            bid 1NT

            # stayman
            ((H == 4 or S == 4) and @points >= 8) or (H >= 4 and S >= 4) or (@points >= 10 and (H == 5 or S == 5) and (H == 4 or S == 4) and (H != S)):
                bid 2C

                H <= 3 and S <= 3:
                    bid 2D

                    @points < 8 and (H > S or (H == S and Hpoints > Spoints)):
                        bid 2H
                        pass

                    @points < 8 and S > H:
                        bid 2S
                        pass

                    @points < 10:
                        bid 2NT
                        # end invite

                    @points >= 10:

                        # smolen
                        S >= 5 and H >= 4:
                            bid 3H
                            # end gf
                        # smolen
                        S == 4 and H >= 5:
                            bid 3S
                            # end gf

                        D >= 5:
                            bid 3D
                            # end gf

                        C >= 5:
                            bid 3C
                            # end gf

                        else:
                            bid 3NT
                            # TODO ?????

                H == 4:
                    bid 2H

                    @points < 8:
                        pass

                    # inwity
                    @points < 10:
                        H == 4:
                            bid  3H
                            # end invite
                        else:
                            bid 2NT
                            # end invite

                    # game force
                    @points >= 10:

                        @points >= 16 and H >= 4:
                            bid 3D  # "szlemikowe uzgodnienie H"
                            # end slam

                        D >= 5:
                            bid 3C
                            # end gf

                        C >= 5:
                            bid 2S
                            # end gf

                        else:
                            bid 3NT  # "pasuj popraw"
                            # end ???

                S == 4:
                    bid 2S

                    @points < 8:
                        pass

                    # inwity
                    @points < 10:

                        S >= 4:
                            bid 3S
                            # end invite

                        else:
                            bid 2NT
                            # end invite

                    # game force
                    @points >= 10:
                        @points >= 16 and S >= 4:
                            bid 3S
                            # end slam

                        D >= 5:
                            bid 3D
                            # end gf

                        C >= 5:
                            bid 3C
                            # end gf

                        else:
                            bid 3NT  # do gry
                            # end ???

            # transfer (teksas) RPA na piki
            S >= 6 and (S + @points >= 14 or AK in H or AQJ in H) and @points <= 10:
                bid 4D

            # transfer (teksas) RPA na kiery
            H >= 6 and (H + @points >= 14 or AK in H or AQJ in H) and @points <= 10:
                bid 4C
                bid 4H

            S >= 6 and (S + @points >= 14 or AK in H or AQJ in H) and @points <= 10:
                bid 4D
                bid 4S

            # trasfer na piki
            S >= 5:
                bid 2H

                # super accept
                @points >= 16 and S >= 4:
                    C == 2:
                        bid 3C
                    D == 2:
                        bid 3D
                    H == 2:
                        bid 3H
                    @points == 17 and $counts == 4333:
                        bid 2NT

                # accept
                else:
                    bid 2S
                    @points < 8:
                        pass

                    # inwity
                    @points < 10:
                        S >= 6:
                            bid 3S
                        H >= 4:
                            bid 3H
                        else:
                            bid 2NT

                    # game force
                    @points >= 10:
                        S > 5 and @points > 12:
                            C < 2:
                                bid 4C
                            D <2:
                                bid 4D
                            H < 2:
                                bid 4H
                            @points > 16:
                                bid 4S
                        D > 4:
                            bid 3D
                        C >= 4:
                            bid 3C
                        2==2:
                            bid 3NT


            # trasfer na kiery
            H >= 5:
                bid 2D

                # supper accept
                @points >= 16 and H >= 4:
                    S == 2:
                        bid 2S
                    C == 2:
                        bid 3C
                    D == 2:
                        bid 3D
                    @points == 17 and $counts == 4333:
                        bid 2NT

                # accept
                2==2:
                    bid 2H

                    @points < 8:
                        pass

                    # inwity
                    @points < 10:
                        H >= 6:
                            bid 3H
                        S == 4:
                            bid 2S
                        2==2:
                            bid 2NT
                    # game force
                    @points >= 10:
                        H > 5 and @points > 12:
                            S < 2:
                                bid 3S
                            C < 2:
                                bid 4C
                            D <2:
                                bid 4D
                            @points > 16:
                                bid 4H
                        D > 4:
                            bid 3D
                        C >= 4:
                            bid 3C
                        2==2:
                            bid 3NT







            C >= 6 and 2 * C + 0.5 * Cpoints + @points >= 29.5 and @points < 15:
                bid 4H
                # slam
                # end

            D >= 6 and 2 * D + 0.5 * Dpoints + @points >= 29.5 and @points < 15:
                bid 4S
                # slam
                # end

            # nie ma inwitu po 1NT - 2NT. Inwity idą przez 1NT - 2S
            D >= 5 and C >= 5 and @points != 8 and @points != 9:
                bid 2NT

                D > C or (D == C and Dpoints > Cpoints):
                    bid 3D

                    @points < 10:
                        pass

                    # gameforce?
                    # end

                else:
                    bid 3C

                    @points < 10:
                        pass

                    # gameforce?
                    # end

            @points == 8 or @points == 9 or C >= 6:
                bid 2S

                # dół otwarcia
                @points == 15:
                    bid 2NT

                # góra otwarcia
                @points > 15:
                    bid 3C

            D >= 6:
                bid 3C
                bid 3D
                # end


            $counts == 5431 and H == 1 and S == 3 and @points >= 10:
                bid 3H
                # end

            $counts == 5431 and H == 3 and S == 1 and @points >= 10:
                bid 3S
                # end

            H == 3 or S == 3 and @points >= 10 and $balance == 0:
                bid 3D

                S >= 5 and (S > H or (H == S and Spoints >= Hpoints)):
                    bid 3S
                    # gameforce
                    # end

                H >= 5:
                    bid 3H
                    # gameforce
                    # end

                else:
                    bid 3NT

            @points >= 10 and @points <= 15:
                bid 3NT
                # end

            @points == 16 or @points == 17:
                bid 4NT
                # end

            @points == 18:
                bid 6NT
                # end

            @points == 19 or @points == 20:
                bid 5NT
                # end

            else:
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




