from Grammar import NON_TERMINATOR, TERMINATOR
from ExpressionFirstFinding import find_first


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

    def isInItem(self, non_terminator, expression, forward_sym):
        """
        在项目集规范族中判断是否已经存在一个类似的产生式。
        """
        for existing_symbol, existing_production, existing_fir_set in self.content:
            if existing_symbol == non_terminator and existing_production == expression and existing_fir_set == forward_sym:
                return True
        return False


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
        self.item_first_production_list = []

    def insertExgrammar(self, index, non_terminator, expression):
        self.exgrammar.append(tuple([index, non_terminator, expression]))

    def insertSpecFamilyItem(self, specFamilyItem):
        self.content.append(specFamilyItem)

    def insertItemFirstProduction(self, non_terminator, production, forward_sym, status):
        # 这张列表将会记录每一个状态集首个产生式的左侧，右部，前看符号，以及状态：status
        self.item_first_production_list.append(tuple([non_terminator, production, forward_sym, status]))

    def isInItemFirstProduction(self, non_terminator, production, forward_sym):
        # 判断传入的产生式是否已经在某个项目集中出现过
        for existing_symbol, existing_production, existing_fir_set, _ in self.item_first_production_list:
            if existing_symbol == non_terminator and existing_production == production and existing_fir_set == forward_sym:
                # 如出现过则返回对应的状态号，否则返回false
                status = _
                return status
        return False

    def get_new_state(self):
        # 获取最新项目集编号
        new_state = max(item[-1] for item in self.item_first_production_list)

        return new_state

    def extendedGrammar(self):
        """
        将传入的文法进行匹配扩充: 扩广文法
        """
        index = 0
        for lp, rp_tuple in self.grammar.items():
            for rp in rp_tuple:
                self.insertExgrammar(index, lp, rp)
                index += 1

    def closureItem(self, specFamilyItem):
        for each_grammar in specFamilyItem.content:
            # 遍历单个项目集中的每一个产生式
            production = each_grammar[1]  # 产生式右部
            fir_sym = each_grammar[2]  #
            caret_index = production.index('^')
            if caret_index < len(production) - 1:
                # 确保 '^' 不是最后一个元素
                symbol = production[caret_index + 1]  # 取^符号后面的操作符
                if symbol in NON_TERMINATOR:
                    # 是非终结符
                    for grammar in self.exgrammar:
                        # 对所有的文法，碰到以该符号开头的文法，则加入到项目集
                        if symbol == grammar[1]:
                            right_production = grammar[2].copy()
                            right_production.insert(0, '^')
                            if caret_index + 1 < len(production) - 1:
                                # 如果求闭包的产生式的'^'后面的元素不是最后一个元素
                                fir_sym_set = find_first([production[-1], fir_sym])
                            else:
                                # 如果 ^ 后面的元素是最后一个
                                fir_sym_set = fir_sym
                            if specFamilyItem.isInItem(symbol, right_production, fir_sym_set) == False:
                                # 不在当前项目集规范组，则添加
                                specFamilyItem.insertContent(symbol, right_production, list(fir_sym_set))
                            else:
                                # 存在当前项目集规范组
                                pass
                else:
                    # 非终结符忽略
                    pass
            else:
                # 如果是最后一个元素，则不用求闭包，直接pass
                pass

    def getTransform(self, specFamilyItem, status):
        for each_production in specFamilyItem.content:
            non_terminator = each_production[0]
            production = each_production[1].copy()
            fir_set = each_production[2]
            caret_index = production.index('^')
            if caret_index + 1 <= len(production) - 1:
                # ^ 不在产生式末尾
                receive_operator = production[caret_index + 1]
                production_move = move_caret(production)
                sate = self.isInItemFirstProduction(non_terminator, production_move, fir_set)
                if sate == False:
                    # 不在项目集的首部
                    new_status = self.get_new_state() + 1
                    specFamilyItem.insertTransfrom(receive_operator, new_status)
                    self.insertItemFirstProduction(non_terminator, production_move, fir_set, new_status)

                else:
                    specFamilyItem.insertTransfrom(receive_operator, sate)
            else:
                # ^ 已经到了产生式末尾
                pass

        ...

    def computeSpecFamilyItem(self):
        # 计算项目集规范族
        self.extendedGrammar()

        first_grammar = self.exgrammar[0]
        right_production = first_grammar[2].copy()
        right_production.insert(0, '^')
        fir_sym = '$'
        state = 0
        self.insertItemFirstProduction(non_terminator=first_grammar[1], production=right_production,
                                       forward_sym=fir_sym, status=state)
        for each_first_production in self.item_first_production_list:
            non_terminator = each_first_production[0]
            production = each_first_production[1]
            forward_sym = each_first_production[2]
            state = each_first_production[3]

            if state == 2:
                print('breakpoint')

            sfi = SpecFamilyItem(state)
            sfi.insertContent(non_terminator=non_terminator, expression=production, forward_sym=forward_sym)
            self.closureItem(sfi)
            self.getTransform(sfi, state)
            self.insertSpecFamilyItem(sfi)
