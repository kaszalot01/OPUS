from opusanalyzer import System
from lark import Tree
def test_blas_parses():
    system = System.load('blas.ol')

    for b in system.branches:
        for c in b.children_iterator():
            assert not isinstance(c, Tree)