from .Grammar import GRAMMAR_WITH_EPSILON

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


def recursive_first_finding(current_non_terminator, non_terminator_in, grammar_in):
    # decisions = GRAMMAR.get(current_non_terminator)
    decisions = grammar_in.get(current_non_terminator)
    if decisions:
        for decision in decisions:
            # 常规操作
            first_sym = decision[0]
            if first_sym in non_terminator_in:
                recursive_first_finding(first_sym, non_terminator_in, grammar_in)
                # 此非终结符是可能为空的
                if is_this_non_terminator_nullable(first_sym, non_terminator_in, grammar_in) and len(decision) > 1:
                    recursive_first_finding(decision[1], non_terminator_in, grammar_in)
            else:
                first.add(first_sym)


def is_this_non_terminator_nullable(target_non_terminator, non_terminator_in, grammar_in):
    # decisions = GRAMMAR.get(target_non_terminator)
    decisions = grammar_in.get(target_non_terminator)
    if decisions:
        for decision in decisions:
            first_sym = decision[0]
            if first_sym == 'ε':
                return True
    return False


def find_first(expression, non_terminator_in, grammar_in):
    first_sym = expression[0]
    if first_sym in non_terminator_in:
        recursive_first_finding(first_sym, non_terminator_in, grammar_in)
        if is_this_non_terminator_nullable(first_sym, non_terminator_in, grammar_in) and len(expression) > 1:
            if expression[1] == '$':
                first.add('$')
            else:
                recursive_first_finding(expression[1], non_terminator_in, grammar_in)
    else:
        first.add(first_sym)

    first.discard('ε')
    return first

