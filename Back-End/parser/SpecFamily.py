from Grammar import NON_TERMINATOR, TERMINATOR


def move_caret(right_production) -> list:
    caret_index = right_production.index('^')

    # 后移'^'
    if caret_index < len(right_production) - 1:  # 确保'^'不是最后一个元素
        right_production[caret_index], right_production[caret_index + 1] = right_production[caret_index + 1], \
            right_production[caret_index]

    return right_production


"""
SpecFamilyItem 的结构例子
{
    "state": 0,
    "content":[
        ("S_",["^","S"],["$"]),
        ("S",["^","B","B"],["$"]),
        ("B",["^","S"],["a","b"]),
        ("B",["^","$"],["a","b"])
    ],
    "transform":{
        "S":1,
        "B":2,
        "b":3,
        "a":4
    }
}
"""


class SpecFamilyItem:
    def __init__(self, state):
        self.state = state
        self.content = list()
        self.transfrom = dict()

    def insertContent(self, non_terminator, expression, forward_sym):
        self.content.append(tuple([non_terminator, expression, forward_sym]))

    def insertTransfrom(self, non_terminator, destination_state):
        self.transfrom[non_terminator] = destination_state


"""
SpecFamily 的结构例子
{
    "exgrammar": [
        (0,"S_",["S"]),
        (1,"S",["B","B"]),
        (2,"B",["b","B"]),
        (3,"B",["a"]),
    ]
    "grammar":{
        'S_': (['S'],),
        'S': (['B', 'B']),
        'B': (['b', 'B'], ['a'],),
    }
    "content":[
        SpecFamilyItem(),
        SpecFamilyItem(),
        SpecFamilyItem(),
        SpecFamilyItem(),
        SpecFamilyItem()
        ...
    ]
}
"""


class SpecFamily:

    def __init__(self, grammar):
        # exgrammar 指的是编码后的拓广文法
        self.grammar = grammar
        self.exgrammar = []
        self.content = []

    def insertExgrammar(self, index, non_terminator, expression):
        self.exgrammar.append(tuple([index, non_terminator, expression]))

    def insertSpecFamilyItem(self, specFamilyItem):
        self.content.append(specFamilyItem)

    def extendedGrammar(self):
        """
        将传入的文法进行匹配扩充
        """
        index = 0
        for lp, rp_tuple in self.grammar.items():
            for rp in rp_tuple:
                self.insertExgrammar(index, lp, rp)
                index += 1

    def closureItem(self, specFamilyItem):
        for each_grammar in specFamilyItem.content:
            production = each_grammar[1]
            caret_index = production.index('^')
            if caret_index < len(production) - 1:
                # 确保不是最后一个元素
                symbol = production[caret_index + 1] # 取^符号后面的操作符
                if symbol in NON_TERMINATOR:
                    # 是非终结符
                    for grammar in self.exgrammar:
                        # 对所有的文法，碰到以该符号开头的文法，则加入到项目集
                        if symbol == grammar[1]:
                            right_production = grammar[2].insert(0, '^')




        ...

    def computeSpecFamilyItem(self):
        self.extendedGrammar()
        first_grammar = self.exgrammar[0]
        fir_right = first_grammar[2].insert(0, '^')
        fir_sym = '$'
        state = 0
        sfi = SpecFamilyItem(state)
        sfi.insertContent(non_terminator=first_grammar[1], expression=fir_right, forward_sym=fir_sym)

        ...
