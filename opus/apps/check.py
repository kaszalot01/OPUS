import sys

from opus.lang.exceptions import TOKENNAME_TO_READABLE, UnexpectedToken

from opus.lang.ir import System


def check_parse(fname):
    try:
        _ = System.load(fname)
    except UnexpectedToken as e:
        print(e, file=sys.stderr)
        exit(1)
