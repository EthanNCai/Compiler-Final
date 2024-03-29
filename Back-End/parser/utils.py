import itertools
from SpecFamily import SpecFamily
from Grammar import GRAMMAR, GRAMMAR_WITH_EPSILON, PL0_GRAMMAR
from Grammar import PL0_NON_TERMINATOR

"""
G[S_]:
        S_ → S
        S  → BB
        B  → bB|a
"""

NON_TERMINATOR_LIST = ['S_', 'S', 'B']
TERMINATORS_LIST = ['a', 'b']

first = {
    'S': set(),
    'S_': set(),
    'B': set()
}

follow = {
    'S': set(),
    'S_': set(),
    'B': set()
}

non_terminator_counts = len(NON_TERMINATOR_LIST)
nullable_non_terminator = []


def find_first(target_non_terminator, current_non_terminator):
    decisions = GRAMMAR.get(current_non_terminator)
    for decision in decisions:
        first_sym = decision[0]
        if first_sym in NON_TERMINATOR_LIST:
            find_first(target_non_terminator, first_sym)
        else:
            first[target_non_terminator].add(first_sym)


def find_follow(begin_non_terminator):
    follow[begin_non_terminator].add('$')

    search_list = list(itertools.product(NON_TERMINATOR_LIST, NON_TERMINATOR_LIST))

    subset_relationships = set()
    for non_terminator_, non_terminator_to_search in search_list:
        decisions = GRAMMAR.get(non_terminator_to_search)

        for decision in decisions:

            index = find_index(non_terminator_, decision)
            if index is None:
                continue

            for i in index:
                if i == len(decision) - 1:
                    subset_relationships.add((non_terminator_, non_terminator_to_search))
                    continue

                if backward_nullable(decision[i + 1:]):
                    subset_relationships.add((non_terminator_, non_terminator_to_search))
                if i != len(decision) - 1:
                    next_symbol = decision[i + 1]
                    if next_symbol in TERMINATORS_LIST:

                        follow[non_terminator_].add(next_symbol)
                    elif next_symbol in NON_TERMINATOR_LIST:

                        follow[non_terminator_].update(first[next_symbol])
                        follow[non_terminator_].discard('ε')

    for i in range(non_terminator_counts):
        for subset_relationship in subset_relationships:
            _set_, subset = subset_relationship
            follow[_set_].update(set(follow[subset]))


def backward_nullable(backward_list):
    return set(backward_list).issubset(set(nullable_non_terminator))


def find_index(target, _list):
    if target in _list:
        return [i for i, x in enumerate(_list) if x == target]
    else:
        return None


def closure(grammar):
    sf = SpecFamily(grammar, PL0_NON_TERMINATOR)
    for each_list in sf.content:
        print('The grammar:')
        for content in each_list.content:
            print(content)
        print('State: ', each_list.state)
        print('Transform: ', each_list.transfrom)
        print('----------------------------')


if __name__ == '__main__':
    # GRAMMAR = GRAMMAR
    # GRAMMAR = GRAMMAR_WITH_EPSILON
    GRAMMAR = PL0_GRAMMAR
    closure(GRAMMAR)
