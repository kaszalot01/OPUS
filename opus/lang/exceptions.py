from collections import UserDict
import lark


class IdentityDict(UserDict):
    def __getitem__(self, item):
        if (res := self.data.get(item)) is None:
            return item
        else:
            return res


TOKENNAME_TO_READABLE = IdentityDict({
    'AT': '@',
    'CLUB_SIGN': '♣',
    'DIAMOND_SIGN': '♦',
    'HEART_SIGN': '♥',
    'SPADE_SIGN': '♠',
    'DOLLAR': '$',
    'LPAR': '(',
    'RPAR': ')',
    'COLON': ':',
    'PLUS': '+',
    'MINUS': '-',
    'STAR': '*',
    'SLASH': '/',
    'MORETHAN': '>',
    'MOREEQTHAN': '>=',
    'LESSTHAN': '<',
    'LESSEQTHAN': '<=',
    'EQUALS': '==',
    'NOTEQUALS': '!='
})


class UnexpectedToken(Exception):

    def __init__(self, lark_exception, *args):
        super().__init__(*args)
        self.lark_exception = lark_exception

    @classmethod
    def from_lark(cls, e: lark.UnexpectedToken):
        msg = f"Unexpected token {e.token!r} at line {e.line}, column {e.column}\n"
        msg += "Expected one of:\n"
        pretty = map(TOKENNAME_TO_READABLE.__getitem__, e.expected)
        expected = sorted(pretty)
        for t in expected:
            msg += "\t" + TOKENNAME_TO_READABLE[t] + '\n'
        return cls(e, msg)


class SystemIncompleteException(Exception):
    pass
