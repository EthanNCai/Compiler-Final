import copy

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

def recursive_first_finding(current_non_terminator, g_pack):
    non_terminator_in, grammar_in, terminator_in = g_pack
    decisions = grammar_in.get(current_non_terminator)
    for decision in decisions:
        # 常规操作
        first_sym = decision[0]
        if first_sym in terminator_in or first_sym in ['$', 'ε']:
            first.add(first_sym)
        elif first_sym in non_terminator_in and current_non_terminator != first_sym:
            recursive_first_finding(first_sym, g_pack)


def _find_first(expression_in, non_terminator_in, grammar_in, terminator_in):
    first.clear()
    expression = copy.deepcopy(expression_in)
    g_pack = (non_terminator_in, grammar_in, terminator_in)
    first_sym = expression[0]

    # 终结符或者是 Dollar
    if first_sym in terminator_in or first_sym in ['$', 'ε']:
        first.add(first_sym)
    # 非终结符
    elif first_sym in non_terminator_in:
        recursive_first_finding(first_sym, g_pack)
    return first
