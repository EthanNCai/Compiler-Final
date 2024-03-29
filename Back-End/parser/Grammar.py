NON_TERMINATOR = ['S_', 'S', 'B']
TERMINATOR = ['a', 'b']
GRAMMAR = {
    'S_': (['S'],),
    'S': (['B', 'B'],),
    'B': (['b', 'B'], ['a'],),
}

GRAMMAR_WITH_EPSILON = {
    'S_': (['S'],),
    'S': (['B', 'B'],),
    'B': (['b', 'B'], ['a'], ['b', 'S'], ['ε'],),
}

PM_GRAMMAR = {
    'S_': (['S'],),
    'S': (['A', 'a'], ['b', 'A', 'c'], ['d', 'c'], ['b', 'd', 'a'],),
    'A': (['d'],),
}
PM_NON_TERMINATOR = ['S_', 'S', 'A']
PM_TERMINATOR = ['a', 'b', 'c', 'd']

# 警告对于'S_': (['S'],), 其 ] 后面的 , 是不可省略的!
# 警告对于'S_': (['S'],), 其 ']' 后面的 ',' 是不可省略的!

first = {
    'S': set(),
    'S_': set(),
    'B': set()
}

follow = {
    'S': set(),
    'S_': set(),
    'B': set()
}

"""
NON_TERMINATOR = ['E', 'T', 'F']
TERMINATOR = ['+','*','(',')','id']

GRAMMAR = {
    'E':(['E','+','T'],['T']),
    'T':(['T','*','F'],['F']),
    'F':(['(','E',')'],['id'])
}
"""
PL0_NON_TERMINATOR_NEW = ['PROG_',
                          'PROG', 'SUBPROG', 'M_STATEMENT', 'CONST', 'CONST_', 'CONST_DEF', 'ID', 'UINT',
                          'VARIABLE', 'VARIABLE_', 'PROCEDURE', 'PROCEDURE_', 'PROC_HEAD',
                          'STATEMENT', 'ASSIGN', 'COMP', 'COMP_BEGIN', 'COND', 'M_COND', 'CONDITION',
                          'EXPR', 'ITEM', 'FACTOR', 'PLUS_MINUS', 'MUL_DIV', 'REL', 'CALL',
                          'WHILE', 'M_WHILE_FORE', 'M_WHILE_TAIL', 'READ', 'READ_BEGIN', 'WRITE', 'WRITE_BEGIN'
                          ]
PL0_TERMINATOR_NEW = [
    '.', ';', 'const', ',', ':=', 'num', 'var', 'id', 'procedure', 'begin', 'end',
    'if', 'then', 'odd', '+', '-', '*', '/', '=', '#', '<', '<=', '>', '>=', 'call',
    'while', 'do', 'read', '(', ')', 'write', '^'
]
PL0_GRAMMAR = {
    'PROG_': (['PROG', '.'],),
    'PROG': (['SUBPROG'],),  #
    'SUBPROG': (['CONST', 'VARIABLE', 'PROCEDURE', 'M_STATEMENT', 'STATEMENT'],),  #
    'M_STATEMENT': (['ε'],),  #
    'CONST': (['CONST_', ';'], ['ε']),  #
    'CONST_': (['CONST_', ',', 'CONST_DEF'], ['const', 'CONST_DEF']),
    'CONST_DEF': (['ID', '=', 'UINT'],),
    'UINT': (['num'],),
    'VARIABLE': (['VARIABLE_', ';'], ['ε']),  #
    'VARIABLE_': (['var', 'ID'], ['VARIABLE_', ',', 'ID']),
    'ID': (['id'],),
    'PROCEDURE': (['PROCEDURE_'], ['ε']),  #
    'PROCEDURE_': (['PROCEDURE_', 'PROC_HEAD', 'SUBPROG', ';'], ['PROC_HEAD', 'SUBPROG', ';']),
    'PROC_HEAD': (['procedure', 'ID', ';'],),
    'STATEMENT': (['ASSIGN'], ['COND'], ['WHILE'], ['CALL'], ['READ'], ['WRITE'], ['COMP'], ['ε']),
    'ASSIGN': (['ID', ':=', 'EXPR'],),
    'COMP': (['COMP_BEGIN', 'end'],),
    'COMP_BEGIN': (['begin', 'STATEMENT'], ['COMP_BEGIN', ';', 'STATEMENT']),
    'COND': (['if', 'CONDITION', 'then', 'M_COND', 'STATEMENT'],),
    'M_COND': (['ε'],),  #
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

"""
PL0_TERMINATOR_NEW = [
    '.', ';', 'const', ',', '=', 'num', 'var', 'id', 'procedure', 'begin', 'end',
    'if', 'then', 'odd', '+', '-', '*', '/', '=', '#', '<', '<=', '>', '>=', 'call',
    'while', 'do', 'read', '(', ')', 'write', '^'
]
"""


def token_to_terminator_bb(token):
    if token == 22:
        return 'a'
    if token == 21:
        return 'b'

    print('ERROR!')


def token_to_terminator_pl0(token):
    if token == 0:
        return ' '
    if token == 1:
        return 'id'
    if token == 2:
        return 'num'
    if token == 3:
        return '+'
    if token == 4:
        return '-'
    if token == 5:
        return '*'
    if token == 6:
        return '/'
    if token == 7:
        return '='
    if token == 8:
        return '>'
    if token == 9:
        return '<'
    if token == 10:
        return '<>'
    if token == 11:
        return '<='
    if token == 12:
        return '>='
    if token == 13:
        return '('
    if token == 14:
        return ')'
    if token == 15:
        return '{'
    if token == 16:
        return '}'
    if token == 17:
        return ';'
    if token == 18:
        return ','
    if token == 19:
        return '"'
    if token == 20:
        return ':='
    if token == 21:
        return 'var'
    if token == 22:
        return 'if'
    if token == 23:
        return 'then'
    if token == 24:
        return 'else'
    if token == 25:
        return 'while'
    if token == 26:
        return 'for'
    if token == 27:
        return 'begin'
    if token == 28:
        return 'writeln'
    if token == 29:
        return 'procedure'
    if token == 30:
        return 'end'
    if token == 33:
        return '.'
    if token == 100:
        return '出错'

    print('ERROR!')
