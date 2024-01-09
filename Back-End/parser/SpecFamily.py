from parser.ExpressionFirstFinding import find_first

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
        判断是否当前产生式是否在当前项目集。
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

    def __init__(self, grammar, non_terminator):
        # exgrammar 指的是编码后的拓广文法
        self.grammar = grammar
        self.non_terminator_in = non_terminator
        self.exgrammar = []
        self.content = []
        self.item_first_production_dict_list = []
        self.computeSpecFamily()

    def insertExgrammar(self, index, non_terminator, expression):
        self.exgrammar.append(tuple([index, non_terminator, expression]))

    def insertSpecFamilyItem(self, specFamilyItem):
        self.content.append(specFamilyItem)

    def insertItemFirstProduction(self, non_terminator, production, forward_sym, status):
        # 这张列表将会记录每一个状态集的初始产生式：{status：[产生式的左侧，右部，前看符号}
        first_production_dict = {status: [non_terminator, production, forward_sym]}
        self.item_first_production_dict_list.append(first_production_dict)

    def isInItemFirstProduction(self, non_terminator, production, forward_sym):
        # 判断传入的产生式是否已经在某个项目集中出现过
        for item in self.item_first_production_dict_list:
            for status, production_info in item.items():
                existing_symbol, existing_production, existing_fir_set = production_info
                if existing_symbol == non_terminator and existing_production == production and existing_fir_set == forward_sym:
                    # 如出现过则返回对应的状态号
                    return status
        return False

    def get_new_state(self):
        # 获取最新项目集编号
        new_state = max(status for item in self.item_first_production_dict_list for status in item.keys())

        return new_state

    def move_caret(self, right_production) -> list:
        """
        移位函数，负责将点 ‘^’ 符号往后移动一位
        :param right_production: 表达式
        :return: 移动以后的表达式
        """
        caret_index = right_production.index('^')

        # 后移'^'
        if caret_index < len(right_production) - 1:  # 确保'^'不是最后一个元素
            right_production[caret_index], right_production[caret_index + 1] = right_production[caret_index + 1], \
                right_production[caret_index]

        return right_production

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
        """
        计算单个项目集的闭包
        :param specFamilyItem: 传入一个项目集，注意是单个项目集
        """
        for each_grammar in specFamilyItem.content:
            # 遍历单个项目集中的每一个产生式
            production = each_grammar[1]  # 产生式右部
            fir_sym = each_grammar[2]  #
            caret_index = production.index('^')
            if caret_index < len(production) - 1:
                # 确保 '^' 不是最后一个元素
                symbol = production[caret_index + 1]  # 取^符号后面的操作符
                if symbol in self.non_terminator_in:
                    # 是非终结符
                    for grammar in self.exgrammar:
                        # 对所有的文法，碰到以该符号开头的文法，则加入到项目集
                        if symbol == grammar[1]:
                            right_production = grammar[2].copy()

                            if right_production[0] == 'ε':
                                # 空集特别考虑， 直接将 'ε' 替换成 '^'
                                right_production[0] = '^'
                            else:
                                right_production.insert(0, '^')

                            if caret_index + 1 < len(production) - 1:
                                # 如果求闭包的产生式的'^'后面的元素不是最后一个元素
                                # print(*fir_sym)
                                fir_sym_set = find_first([production[-1], *fir_sym], self.non_terminator_in,
                                                         self.grammar)
                            else:
                                # 如果 ^ 后面的元素是最后一个
                                fir_sym_set = fir_sym
                            if not specFamilyItem.isInItem(symbol, right_production, fir_sym_set):
                                # 不在当前项目集，则添加
                                # print('breakpoint')
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

    def getTransform(self, specFamilyItem):
        """
        计算当前状态集的转换状态集及接受字符
        """
        for each_production in specFamilyItem.content:
            non_terminator = each_production[0]
            production = each_production[1].copy()
            fir_set = each_production[2]
            caret_index = production.index('^')
            if caret_index + 1 <= len(production) - 1:
                # ^ 不在产生式末尾
                receive_operator = production[caret_index + 1]
                production_move = self.move_caret(production)
                sate = self.isInItemFirstProduction(non_terminator, production_move, fir_set)
                if sate == False:
                    # 不在项目集的首部
                    if receive_operator in specFamilyItem.transfrom:
                        new_status = specFamilyItem.transfrom[receive_operator]
                    else:
                        new_status = self.get_new_state() + 1
                        specFamilyItem.insertTransfrom(receive_operator, new_status)
                    self.insertItemFirstProduction(non_terminator, production_move, list(fir_set), new_status)

                else:
                    specFamilyItem.insertTransfrom(receive_operator, sate)
            else:
                # ^ 已经到了产生式末尾
                pass

    def computeSpecFamily(self):
        self.extendedGrammar()
        first_grammar = self.exgrammar[0]
        right_production = first_grammar[2].copy()
        right_production.insert(0, '^')
        fir_sym = '$'
        state = 0
        self.insertItemFirstProduction(non_terminator=first_grammar[1], production=right_production,
                                       forward_sym=fir_sym, status=state)
        for item in self.item_first_production_dict_list:
            for state, production_info in item.items():
                non_terminator, production, forward_sym = production_info
                if self.content:
                    flag = False
                    for each_item in self.content:
                        if state == each_item.state:
                            sfi = each_item
                            flag = True
                            break
                    if (flag == False):
                        sfi = SpecFamilyItem(state)
                else:
                    # 对初始状态集I0直接创建一个项目集
                    sfi = SpecFamilyItem(state)
                sfi.insertContent(non_terminator=non_terminator, expression=production, forward_sym=list(forward_sym))
                self.closureItem(sfi)
                self.getTransform(sfi)
                self.insertSpecFamilyItem(sfi)

