from parser.Grammar import GRAMMAR
from parser.SpecFamily import SpecFamily


def first():
    return


def follow():
    return


def closure(grammar):
    sf = SpecFamily(grammar)
    sf.extendedGrammar()
    ...


if __name__ == '__main__':
    grammar = GRAMMAR
    closure(grammar)
