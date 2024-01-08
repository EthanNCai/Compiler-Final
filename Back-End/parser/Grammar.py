NON_TERMINATOR = ['S_', 'S', 'B']
TERMINATOR = ['a', 'b']

GRAMMAR = {
    'S_': (['S'],),
    'S': (['B', 'B']),
    'B': (['b', 'B'], ['a'],),
}

# 警告对于'S_': (['S'],), 其 ] 后面的 , 是不可省略的!
