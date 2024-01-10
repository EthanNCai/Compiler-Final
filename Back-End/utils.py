import itertools
import copy
from parser.ReturnNullableList import _find_first
from parser.SpecFamily import SpecFamily
from parser.Grammar import GRAMMAR, GRAMMAR_WITH_EPSILON, PL0_GRAMMAR
from parser.ExpressionFirstFinding import find_first

"""
G[S_]:
        S_ → S
        S  → BB
        B  → bB|a
"""

PL0_NON_TERMINATOR_NEW = ['PROG_',
                          'PROG', 'SUBPROG', 'M_STATEMENT', 'CONST', 'CONST_', 'CONST_DEF', 'UINT',
                          'VARIABLE', 'VARIABLE_', 'ID', 'PROCEDURE', 'PROCEDURE_', 'PROC_HEAD',
                          'STATEMENT', 'ASSIGN', 'COMP', 'COMP_BEGIN', 'COND', 'M_COND', 'CONDITION',
                          'EXPR', 'ITEM', 'FACTOR', 'PLUS_MINUS', 'MUL_DIV', 'REL', 'CALL',
                          'WHILE', 'M_WHILE_FORE', 'M_WHILE_TAIL', 'READ', 'READ_BEGIN', 'WRITE', 'WRITE_BEGIN'
                          ]

PL0_TERMINATOR_NEW = [
    '.', ';', 'const', ',', '=', 'num', 'var', 'id', 'procedure', 'begin', 'end',
    'if', 'then', 'odd', '+', '-', '*', '/', '=', '#', '<', '<=', '>', '>=', 'call',
    'while', 'do', 'read', '(', ')', 'write', '^'
]

non_terminator_counts = len(PL0_NON_TERMINATOR_NEW)

nullable_non_terminator = set()

first = {
    'PROG_': set(),
    'PROG': set(),  #
    'SUBPROG': set(),  #
    'M_STATEMENT': set(),  #
    'CONST': set(),  #
    'CONST_': set(),
    'CONST_DEF': set(),
    'UINT': set(),
    'VARIABLE': set(),  #
    'VARIABLE_': set(),
    'ID': set(),
    'PROCEDURE': set(),  #
    'PROCEDURE_': set(),
    'PROC_HEAD': set(),
    'STATEMENT': set(),
    'ASSIGN': set(),
    'COMP': set(),
    'COMP_BEGIN': set(),
    'COND': set(),
    'M_COND': set(),  #
    'CONDITION': set(),
    'EXPR': set(),
    'ITEM': set(),
    'FACTOR': set(),
    'PLUS_MINUS': set(),
    'MUL_DIV': set(),
    'REL': set(),
    'CALL': set(),
    'WHILE': set(),
    'M_WHILE_FORE': set(),
    'M_WHILE_TAIL': set(),
    'READ': set(),
    'READ_BEGIN': set(),
    'WRITE': set(),
    'WRITE_BEGIN': set(),
}

follow = {
    'PROG_': set(),
    'PROG': set(),  #
    'SUBPROG': set(),  #
    'M_STATEMENT': set(),  #
    'CONST': set(),  #
    'CONST_': set(),
    'CONST_DEF': set(),
    'UINT': set(),
    'VARIABLE': set(),  #
    'VARIABLE_': set(),
    'ID': set(),
    'PROCEDURE': set(),  #
    'PROCEDURE_': set(),
    'PROC_HEAD': set(),
    'STATEMENT': set(),
    'ASSIGN': set(),
    'COMP': set(),
    'COMP_BEGIN': set(),
    'COND': set(),
    'M_COND': set(),  #
    'CONDITION': set(),
    'EXPR': set(),
    'ITEM': set(),
    'FACTOR': set(),
    'PLUS_MINUS': set(),
    'MUL_DIV': set(),
    'REL': set(),
    'CALL': set(),
    'WHILE': set(),
    'M_WHILE_FORE': set(),
    'M_WHILE_TAIL': set(),
    'READ': set(),
    'READ_BEGIN': set(),
    'WRITE': set(),
    'WRITE_BEGIN': set(),
}

def find_follow(begin_non_terminator):
    follow[begin_non_terminator].add('$')

    search_list = list(itertools.product(PL0_NON_TERMINATOR_NEW, PL0_NON_TERMINATOR_NEW))

    subset_relationships = set()

    for non_terminator_, non_terminator_to_search in search_list:
        # print(non_terminator_to_search)
        decisions = PL0_GRAMMAR.get(non_terminator_to_search)
        # print(decisions)
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
    
                    if next_symbol in PL0_TERMINATOR_NEW:
                        follow[non_terminator_].add(next_symbol)
                    elif next_symbol in PL0_NON_TERMINATOR_NEW:
                        follow[non_terminator_].update(first[next_symbol])
                        follow[non_terminator_].discard('ε')

    for i in range(non_terminator_counts):
        for subset_relationship in subset_relationships:
            _set_, subset = subset_relationship
            follow[_set_].update(set(follow[subset]))
    return follow


def backward_nullable(backward_list):
    return set(backward_list).issubset(set(nullable_non_terminator))


def find_index(target, _list):
    if target in _list:
        return [i for i, x in enumerate(_list) if x == target]
    else:
        return None


def closure(grammar):
    sf = SpecFamily(grammar)
    for each_list in sf.content:
        print('The grammar:')
        for content in each_list.content:
            print(content)
        print('State: ', each_list.state)
        print('Transform: ', each_list.transfrom)
        print('----------------------------')


if __name__ == '__main__':

    # GRAMMAR = GRAMMAR
    GRAMMAR = GRAMMAR_WITH_EPSILON

    for non_terminator in PL0_NON_TERMINATOR_NEW:
        first[non_terminator] = find_first([non_terminator], PL0_NON_TERMINATOR_NEW, PL0_GRAMMAR, PL0_TERMINATOR_NEW)

    print(first)

    find_follow('PROG_')

    print(follow)
    
    #closure(GRAMMAR)
