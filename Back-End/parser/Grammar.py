NON_TERMINATOR = ['S_', 'S', 'B']
TERMINATOR = ['a', 'b']

GRAMMAR = {
    'S_': (['S'],),
    'S': (['B', 'B'],),
    'B': (['b', 'B'], ['a']),
}

GRAMMAR_WITH_EPSILON = {
    'S_': (['S'],),
    'S': (['B', 'B'],),
    'B': (['b', 'B'], ['a'], ['b', 'S'], ['ε']),
}

# 警告对于'S_': (['S'],), 其 ] 后面的 , 是不可省略的!
# 警告对于'S_': (['S'],), 其 ']' 后面的 ',' 是不可省略的!

PL0_NON_TERMINATOR = []
PL0_TERMINATOR = []


PL0_GRAMMAR = {
    'PROG': (['SUBPROG', '.'],),
    'SUBPROG': (['CONST', 'VARIABLE', 'PROCEDURE', 'M_STATEMENT', 'STATEMENT'],),
    'M_STATEMENT': (['ε'],),
    'CONST': (['CONST_', ';'], ['ε']),
    'CONST_': (['CONST_', ',', 'CONST_DEF'], ['const', 'CONST_DEF']),
    'CONST_DEF': (['ID', '=', 'UINT'],),
    'UINT': (['num'],),
    'VARIABLE': (['VARIABLE_', ';'], ['ε'], ['var', 'ID'], ['VARIABLE_', ',', 'ID']),
    'ID': (['id'],),
    'PROCEDURE': (['PROCEDURE_'], ['ε']),
    'PROCEDURE_': (['PROCEDURE_', 'PROC_HEAD', 'SUBPROG', ';'], ['PROC_HEAD', 'SUBPROG', ';']),
    'PROC_HEAD': (['procedure', 'ID', ';'],),
    'STATEMENT': (['ASSIGN'], ['COND'], ['WHILE'], ['CALL'], ['READ'], ['WRITE'], ['COMP'], ['ε']),
    'ASSIGN': (['ID', ':=', 'EXPR'],),
    'COMP': (['COMP_BEGIN', 'end'],),
    'COMP_BEGIN': (['begin', 'STATEMENT'], ['COMP_BEGIN', ';', 'STATEMENT']),
    'COND': (['if', 'CONDITION', 'then', 'M_COND', 'STATEMENT'],),
    'M_COND': (['ε'],),
    'CONDITION': (['EXPR', 'REL', 'EXPR'], ['odd', 'EXPR']),
    'EXPR': (['PLUS_MINUS', 'ITEM'], ['EXPR', 'PLUS_MINUS', 'ITEM'], ['ITEM']),
    'ITEM': (['FACTOR'], ['ITEM', 'MUL_DIV', 'FACTOR'],),
    'FACTOR': (['ID'], ['UINT'], ['(', 'EXPR', ')']),
    'PLUS_MINUS': (['+'], ['-']),
    'MUL_DIV': (['*'], ['/']),
    'REL': (['='], ['#'], ['<'], ['<='], ['>'], ['>=']),
    'CALL': (['call', 'ID'],),
    'WHILE': (['while', 'M_WHILE_FORE', 'CONDITION', 'do', 'M_WHILE_TAIL', 'STATEMENT'],),
    'M_WHILE_FORE': (['ε'],),
    'M_WHILE_TAIL': (['ε'],),
    'READ': (['READ_BEGIN', ')'],),
    'READ_BEGIN': (['read', '(', 'ID'], ['READ_BEGIN', ',', 'ID'],),
    'WRITE': (['WRITE_BEGIN', ')'],),
    'WRITE_BEGIN': (['write', '(', 'ID'], ['WRITE_BEGIN', ',', 'ID']),
}
