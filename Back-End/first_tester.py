from parser.Grammar import token_to_terminator_bb, GRAMMAR_WITH_EPSILON, PL0_NON_TERMINATOR, PL0_GRAMMAR, PL0_TERMINATOR
from parser.ExpressionFirstFinding import find_first

ret = find_first(['CONST', 'VARIABLE', 'PROCEDURE', 'M_STATEMENT', 'STATEMENT', '.'], PL0_NON_TERMINATOR, PL0_GRAMMAR,
           PL0_TERMINATOR)
print(ret)