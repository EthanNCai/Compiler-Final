from Grammar import GRAMMAR, NON_TERMINATOR, TERMINATOR

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


def recursive_first_finding(current_non_terminator):
    decisions = GRAMMAR.get(current_non_terminator)
    for decision in decisions:
        # 常规操作
        first_sym = decision[0]
        if first_sym in NON_TERMINATOR:
            recursive_first_finding(first_sym)
            # 此非终结符是可能为空的
            if is_this_non_terminator_nullable(first_sym) and len(decision) > 1:
                recursive_first_finding(decision[1])
        else:
            first.add(first_sym)


def is_this_non_terminator_nullable(target_non_terminator):
    decisions = GRAMMAR.get(target_non_terminator)
    for decision in decisions:
        first_sym = decision[0]
        if first_sym == 'ε':
            return True
    return False


def find_first(expression):
    first_sym = expression[0]
    if first_sym in NON_TERMINATOR:
        recursive_first_finding(first_sym)
        if is_this_non_terminator_nullable(first_sym) and len(expression) > 1:
            recursive_first_finding(expression[1])
    else:
        first.add(first_sym)
    return first


def main():
    print(find_first(['B', '$']))


if __name__ == '__main__':
    main()
