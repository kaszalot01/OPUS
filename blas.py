from random import randint

def gen_deal():
    import random
    deal = [0, 1, 2, 3] * 13
    random.shuffle(deal)
    return deal


def py_to_LIN(deal):
    plik = open("nazwa", mode='a')
    result = "qx|o1|md|"
    result += str(randint(1,4))
    for i in range(3):
        result += hand(deal,i)
        result += ','
    plik.write(result[:-1])
    plik.write('\n')


def hand(deal, player):
    karty = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')
    result = 'S'
    for k in range(4):
        s = k * 13
        f = (k + 1) * 13
        for i in range(s,f):
            if deal[i] == player:
                result += karty[i % 13]
        if k == 0: result += 'H'
        elif k == 1: result += 'D'
        elif k == 2: result += 'C'
    return result

class Reka:
    def __init__(self, hand):
        self.piki = hand.index("H") - hand.index("S") - 1
        self.kiery = hand.index("D") - hand.index("H") - 1
        self.kara = hand.index("C") - hand.index("D") - 1
        self.trefle = len(hand) - hand.index("C") - 1
        self.kartyPiki = hand[hand.index('S') + 1 : hand.index("H")]
        self.kartyKiery = hand[hand.index('H') + 1: hand.index("D")]
        self.kartyKara = hand[hand.index('D') + 1: hand.index("C")]
        self.kartyTrefle = hand[hand.index('C') + 1:]
        self.punktyTrefle = self.kartyTrefle.count("A") * 4 + self.kartyTrefle.count("K") * 3 + self.kartyTrefle.count("Q") * 2 + self.kartyTrefle.count("J")
        self.punktyKara = self.kartyKara.count("A") * 4 + self.kartyKara.count("K") * 3 + self.kartyKara.count("Q") * 2 + self.kartyKara.count("J")
        self.punktyKiery = self.kartyKiery.count("A") * 4 + self.kartyKiery.count("K") * 3 + self.kartyKiery.count("Q") * 2 + self.kartyKiery.count("J")
        self.punktyPiki = self.kartyPiki.count("A") * 4 + self.kartyPiki.count("K") * 3 + self.kartyPiki.count("Q") * 2 + self.kartyPiki.count("J")
        self.punkty = hand.count("A")*4 + hand.count("K")*3 + hand.count("Q")*2 + hand.count("J")
        uklad = sorted([self.piki, self.kiery, self.kara, self.trefle])[::-1]
        self.uklad = uklad
        if uklad[0] == 4 and uklad[-1] > 1:
            self.zrownowazenie = 2
        elif uklad == [5,3,3,2]:
            self.zrownowazenie = 1
        else: self.zrownowazenie = 0
        self.asy = hand.count("A")
        self.krole = hand.count("K")

x = gen_deal()
y = hand(x,0)
z = Reka(y)
print(y)
print(z.kartyTrefle)

#print(z.piki, z.kiery, z.kara, z.trefle, z.punkty, z.zrownowazenie)

def zmiana(nast):
    if nast == "N": return "S"
    else: return "N"

def licytujacy(N, S, nast):
    if nast == "N": return N
    else: return S

def licytacja(N, S, zal, dealer): # zal jak na bbo
    zapisN = N
    zapisS = S
    N = Reka(N)
    S = Reka(S)
    wynik = ''
    if dealer == 1:
        nast = "S" #nast - nastepny do licytacji
        licznik = 1
    elif dealer == 4:
        nast = "S"
        licznik = 2
    elif dealer == 3:
        nast = "N"
        licznik = 1
    else:
        nast = "N"
        licznik = 2
    if zal == "0":
        pom = licytujacy(N,S,nast)
        if pom.punkty > 21:
            wynik += "2D - "
            nast = zmiana(nast)
            pom = licytujacy(N, S, nast)
            if pom.kiery >= 4 and pom.punkty < 15:
                wynik += "2S - "
            elif pom.punkty in (15,16,17) and pom.piki >= 2 and pom.kiery >= 2:
                wynik += "4C - "
        if pom.zrownowazenie == 1 or pom.zrownowazenie == 2:
            if pom.punkty in (15,16,17):
                wynik += "1NT - "
                nast = zmiana(nast)
                pom = licytujacy(N, S, nast)
                if ((pom.kiery == 4 or pom.piki == 4) and pom.punkty >= 8) or (pom.kiery >= 4 and pom.piki >= 4):
                    wynik += "2C - "
                elif pom.kiery >= 6 and (pom.kiery + pom.punkty >= 14 or pom.kartyKiery[:2] == 'AK' or pom.kartyKiery[:3] == 'AQJ') and pom.punkty <= 10:
                    wynik += "4C - "
                elif pom.piki >= 6 and (pom.piki + pom.punkty >= 14 or pom.kartyPiki[:2] == 'AK' or pom.kartyPiki[:3] == 'AQJ') and pom.punkty <= 10:
                    wynik += "4D - "
                elif pom.kiery >= 5:
                    wynik += "2D - "
                elif pom.piki >= 5:
                    wynik += "2H - "
                elif pom.trefle >= 6 and 2 * pom.trefle + 0.5 * pom.punktyTrefle + pom.punkty >= 29.5 and pom.punkty < 15:
                    wynik += "4H - "
                elif pom.kara >= 6 and 2 * pom.kara + 0.5 * pom.punktyKara + pom.punkty >= 29.5 and pom.punkty < 15:
                    wynik += "4S - "
                elif pom.kara >= 5 and pom.trefle >= 5:
                    wynik += "2NT - "
                elif pom.punkty in (8,9) or pom.trefle >= 6:
                    wynik += "2C - "
                elif pom.kara >= 6:
                    wynik += "3D - "
                elif pom.uklad == [5,4,3,1] and pom.kiery == 1 and pom.piki == 3 and pom.punkty >= 10:
                    wynik += "3H - "
                elif pom.uklad == [5,4,3,1] and pom.kiery == 3 and pom.piki == 1 and pom.punkty >= 10:
                    wynik += "3S - "
                elif pom.kiery == 3 or pom.piki == 3 and pom.punkty >= 10 and pom.zrownowazenie == 0:
                    wynik += "3D - "
                elif pom.punkty in (10,11,12,13,14,15):
                    wynik += "3NT - "
                elif pom.punkty in (16,17):
                    wynik += "4NT - "
                elif pom.punkty == 18:
                    wynik += "6NT"
                elif pom.punkty in (19,20):
                    wynik += "5NT - "
                elif pom.punkty > 20:
                    wynik += "7NT - "
                else: wynik += "Pass - "
            elif pom.punkty < 12:
                wynik += "Pass - "
            elif pom.punkty in (20,21):
                wynik += "2NT - "
                nast = zmiana(nast)
                pom = licytujacy(N, S, nast)
                if pom.trefle >= 5 and pom.kara >= 5 and pom.punkty >= 7:
                    wynik += "3S - "
                elif pom.trefle >= 6 and 2 * pom.trefle + 0.5 * pom.punktyTrefle + pom.punkty >= 24.5:
                    wynik += "4H - "
                elif pom.kara >= 6 and 2 * pom.kara + 0.5 * pom.punktyKara + pom.punkty >= 24.5:
                    wynik += "4S - "


            elif pom.punkty in (12,13,14):
                wynik += "1C - "
            elif pom.kiery == 5:
                wynik += "1H - "
            elif pom.piki == 5:
                wynik += "1S - "
            else:
                wynik += "1C - "
        if pom.punkty <= 9 and pom.punkty >= 5:
            if pom.piki >= 4 and pom.kiery >= 4:
                wynik += "2C - "
            elif pom.kiery == 5 and ( pom.trefle >= 4 or pom.kara >= 4 ):
                wynik += "2H - "
            elif pom.piki == 5 and (pom.trefle >= 4 or pom.kara >= 4):
                wynik += "2S - "
            elif pom.piki == 6 or pom.kiery == 6:
                wynik += "2D - "
            elif pom.piki == 7:
                wynik += "3S - "
            elif pom.piki > 7:
                wynik += "4S - "
            elif pom.kiery == 7:
                wynik += "3H - "
            elif pom.kiery > 7:
                wynik += "4H - "
            elif pom.kara == 7:
                wynik += "3D - "
            elif pom.kara > 7:
                wynik += "4D - "
            elif pom.trefle == 7:
                wynik += "3C - "
            elif pom.trefle > 7:
                wynik += "4C - "
        if pom.punkty in (10,11):
            if pom.piki > 5:
                wynik += "1S - "
            elif pom.kiery > 5:
                wynik += "1H - "
        if pom.punkty >= 12:
            if pom.piki >= 5:
                wynik += "1S - "
            elif pom.kiery >= 5:
                wynik += "1H - "
            elif pom.kara >= 5:
                wynik += "1D - "
            elif pom.trefle >= 5:
                wynik += "1C - "
            elif pom.uklad == [4,4,4,1] and pom.kara != 1:
                wynik += "1C - "
            else: wynik += "1C - "
        else: wynik += "Pass - "
        return wynik


print(licytacja("SAT98HAK8DQJ98CK4",'SJ987HQ76DA3CQJ75', '0', 3)[:8])
#dobra zmiana
print("zmiana"
      "")