from parser.Grammar import token_to_terminator_bb, GRAMMAR_WITH_EPSILON, PM_NON_TERMINATOR, PM_GRAMMAR, PM_TERMINATOR
from parser.ExpressionFirstFinding import find_first

ret = find_first(['A', 'a', ], PM_NON_TERMINATOR, PM_GRAMMAR,
           PM_TERMINATOR)
print(ret)


# 可能推出空串的所有非终结符 {'M_STATEMENT', 'SUBPROG', 'M_WHILE_TAIL', 'VARIABLE', 'CONST', 'PROCEDURE', 'STATEMENT',
# 'M_WHILE_FORE', 'PROG_', 'M_COND', 'PROG'}