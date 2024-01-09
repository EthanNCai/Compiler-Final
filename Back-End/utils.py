import itertools
import copy
from parser.ReturnNullableList import _find_first
from parser.SpecFamily import SpecFamily
from parser.Grammar import GRAMMAR, GRAMMAR_WITH_EPSILON, PL0_GRAMMAR

"""
G[S_]:
        S_ → S
        S  → BB
        B  → bB|a
"""

NON_TERMINATOR_LIST = ['S_', 'S', 'B']
TERMINATORS_LIST = ['a', 'b']

non_terminator_counts = len(NON_TERMINATOR_LIST)

nullable_non_terminator = set()

first_all = {
    'S': set(),
    'S_': set(),
    'B': set()
    }

follow = {
    'S': set(),
    'S_': set(),
    'B': set()
}

first = set()

def recursive_first_finding(current_non_terminator, g_pack):
    non_terminator_in, grammar_in, terminator_in = g_pack

    decisions = grammar_in.get(current_non_terminator)

    if not decisions:
        print(current_non_terminator)
    for decision in decisions:
        # 常规操作
        first_sym = decision[0]
        if first_sym in terminator_in or first_sym in ['$', 'ε']:
            first.add(first_sym)
        elif first_sym in non_terminator_in and first_sym != current_non_terminator:
            recursive_first_finding(first_sym, g_pack)
            # 此非终结符是可能为空的
            if is_this_non_terminator_nullable(first_sym, g_pack) and len(decision) > 1:
                decision.pop(0)
                next_first_sym = decision[0]
                if next_first_sym in terminator_in or next_first_sym in ['$', 'ε']:
                    first.add(next_first_sym)
                else:
                    recursive_first_finding(next_first_sym, g_pack)


def is_this_non_terminator_nullable(target_non_terminator, g_pack):
    if target_non_terminator in nullable_non_terminator:
        return True
    else:
        return False


def find_first(expression_in, non_terminator_in, grammar_in, terminator_in):
    expression = copy.deepcopy(expression_in)
    g_pack = (non_terminator_in, grammar_in, terminator_in)
    generate_nullable_list(g_pack)
    first_sym = expression[0]

    # 终结符或者是 Dollar
    if first_sym in terminator_in or first_sym in ['$', 'ε']:
        first.add(first_sym)
    # 非终结符
    elif first_sym in non_terminator_in:
        # 加入First
        recursive_first_finding(first_sym, g_pack)

        # 如果可以为空的话往后面找
        if is_this_non_terminator_nullable(first_sym, g_pack) and len(expression) > 1:
            expression.pop(0)
            next_first_sym = expression[0]
            if next_first_sym in terminator_in or next_first_sym in ['$', 'ε']:
                first.add(next_first_sym)
            else:
                recursive_first_finding(next_first_sym, g_pack)
    return first


def generate_nullable_list(g_pack):
    non_terminator_in, grammar_in, terminator_in = g_pack
    for non_terminator in non_terminator_in:
        input = [non_terminator, ]
        if 'ε' in _find_first(input, non_terminator_in, grammar_in, terminator_in):
            nullable_non_terminator.update(input)
    #print(nullable_non_terminator)

    
def find_follow(begin_non_terminator):
    follow[begin_non_terminator].add('$')

    search_list = list(itertools.product(NON_TERMINATOR_LIST, NON_TERMINATOR_LIST))

    subset_relationships = set()

    for non_terminator_, non_terminator_to_search in search_list:
        #print(non_terminator_to_search)
        decisions = GRAMMAR_WITH_EPSILON.get(non_terminator_to_search)
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
    
                    if next_symbol in TERMINATORS_LIST:
                        follow[non_terminator_].add(next_symbol)
                    elif next_symbol in NON_TERMINATOR_LIST:
                        follow[non_terminator_].update(first_all[next_symbol])
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

    for non_terminator in NON_TERMINATOR_LIST:
        first_all[non_terminator] = find_first([non_terminator], NON_TERMINATOR_LIST, GRAMMAR_WITH_EPSILON, TERMINATORS_LIST)
    
    print(GRAMMAR_WITH_EPSILON)
    print(first_all)

    find_follow('S_')

    print(follow)
    
    #closure(GRAMMAR)
