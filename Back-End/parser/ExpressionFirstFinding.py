import copy
from .ReturnNullableList import _find_first
from .Grammar import GRAMMAR_WITH_EPSILON
import sys

"""
NON_TERMINATOR = ['E', 'E_', 'T', 'T_', 'F']
TERMINATOR = ['+', '*', '(', ')', 'id']

GRAMMAR = {
    'E': (['T', 'E_'],),
    'E_': (['+', 'T', 'E_'], ['ε']),
    'T': (['F', 'T_'],),
    'T_': (['*', 'F', 'T_'], ['ε']),
    'F': (['(', 'E', ')'], ['id'])
}
"""

"""
使用示例
find_first(['T_', 'F', 'T_'])

输入：一个list
['T_', 'F', 'T_']

返回：一个set
{'(', 'id', '*', 'ε'}
"""

first = set()
nullable_non_terminator = set()


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

