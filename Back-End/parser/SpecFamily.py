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
        self.content.append(tuple(non_terminator, expression, forward_sym))

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

    def insertIndexList(self, index, non_terminator, expression):
        self.exgrammar.append((index, non_terminator, expression))

    def insertSpecFamilyItem(self, specFamilyItem):
        self.content.append(specFamilyItem)

    def extendedGrammar(self):
        """
        将传入的文法进行匹配扩充
        """
        index = 0
        for lp, rp_tuple in self.grammar.items():
            for rp in rp_tuple:
                self.insertIndexList(index, lp, rp)
                index += 1

        for tup in self.exgrammar:
            print(tup)

    def calculateSpecFamilyItem(self):
        ...
