from parser.Grammar import token_to_terminator_bb, GRAMMAR_WITH_EPSILON, PL0_NON_TERMINATOR_NEW, PL0_GRAMMAR, PL0_TERMINATOR_NEW
from parser.ExpressionFirstFinding import find_first

ret = find_first(['VARIABLE', 'PROCEDURE', 'M_STATEMENT', 'STATEMENT', '.'], PL0_NON_TERMINATOR_NEW, PL0_GRAMMAR,
           PL0_TERMINATOR_NEW)
print(ret)


# 可能推出空串的所有非终结符 {'M_STATEMENT', 'SUBPROG', 'M_WHILE_TAIL', 'VARIABLE', 'CONST', 'PROCEDURE', 'STATEMENT',
# 'M_WHILE_FORE', 'PROG_', 'M_COND', 'PROG'}