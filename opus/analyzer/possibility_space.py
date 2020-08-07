from opus.lang.ir import BinaryExpr, InExpr, Atom, Branch, Test


class PossibilitySpace:

    def __init__(self):

        self.points = list(range(0, 41))

        self.clubs_points = list(range(0, 11))
        self.diamonds_points = list(range(0, 11))
        self.hearts_points = list(range(0, 11))
        self.spades_points = list(range(0, 11))

        self.clubs_might = set("AKQJ")
        self.diamonds_might = set("AKQJ")
        self.hearts_might = set("AKQJ")
        self.spades_might = set("AKQJ")

        self.clubs_has = set()
        self.diamonds_has = set()
        self.hearts_has = set()
        self.spades_has = set()

    def adjust(self, test: Test, truth: bool):
        pass

    def _adjust_binexpr(self, test: BinaryExpr, truth: bool):
        pass


