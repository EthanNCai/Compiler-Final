from Grammar import NON_TERMINATOR, TERMINATOR
import copy

"""
分析表的例子它就像下面这样

    ACTION = {
        "0":{
            "b":"S3",
            "a":"S4",
            "$":"E"
        },
        "1":{
            "b":"E",
            "a":"E",
            "$":"A"
        },
        "2":{
            "b":"S6",
            "a":"S7",
            "$":"E"
        },
        "3":{
            "b":"S3",
            "a":"S4",
            "$":"E"
        },
        "4":{
            "b":"R3",
            "a":"R3",
            "$":"E"
        },
        "5":{
            "b":"E",
            "a":"E",
            "$":"R1"
        },
        "6":{
            "b":"S6",
            "a":"S7",
            "$":"E"
        },
        "7":{
            "b":"E",
            "a":"E",
            "$":"R3"
        },
        "8":{
            "b":"R2",
            "a":"R2",
            "$":"E"
        },
        "9":{
            "b":"E",
            "a":"E",
            "$":"R2"
        }
    }


    GOTO = {
        "S":{
            "0":"1",
            "1":"E",
            "2":"E",
            "3":"E",
            "4":"E",
            "5":"E",
            "6":"E",
            "7":"E",
            "8":"E",
            "9":"E"
        },
        "B":{
            "0":"2",
            "1":"E",
            "2":"5",
            "3":"8",
            "4":"E",
            "5":"E",
            "6":"9",
            "7":"E",
            "8":"E",
            "9":"E"
        }
    }

    

"""


class AnalysisTable:

    def __init__(self, specFamily):
        self.specFamily = specFamily
        self.action = dict()
        self.goto = dict()
        self.construct_goto()
        self.construct_action()
        self.isLR1 = True

    def construct_goto(self):
        for specFamilyItem in self.specFamily.content:
            state_index = specFamilyItem.state
            state_transform = specFamilyItem.transfrom
            for input, destination in state_transform.items():
                if input in NON_TERMINATOR:
                    # 填入数字
                    if input not in self.goto:
                        self.goto[input] = dict()
                    self.goto[input][state_index] = destination
                else:
                    # 填入错误标记(此处为空)
                    # if key not in self.goto:
                    #     self.goto[key] = dict()
                    # self.goto[key][state_index] = 'E'
                    ...

    def construct_action(self):

        for specFamilyItem in self.specFamily.content:
            state_index = specFamilyItem.state
            state_content = specFamilyItem.content
            state_transform = specFamilyItem.transfrom
            exGrammar = self.specFamily.exgrammar
            # 加入reduction
            for non_terminator, expression, forward_syms in state_content:
                if expression[-1] == "^":

                    # 找到这个项目
                    exp_to_match = copy.deepcopy(expression)
                    exp_to_match.pop()
                    exGrammarIndex = -1
                    for exp_a_index, _, exp_a in exGrammar:
                        if exp_a == exp_to_match:
                            exGrammarIndex = exp_a_index
                    if exGrammarIndex == -1:
                        print("ERROR")
                    for forward_sym in forward_syms:
                        if state_index not in self.action:
                            self.action[state_index] = dict()
                        if exGrammarIndex == 0:
                            self.action[state_index][forward_sym] = 'ACC'
                            continue
                        # 检查这一格是否已经有项目了（说明冲突）
                        if forward_sym in self.action[state_index]:
                            self.isLR1 = False
                        self.action[state_index][forward_sym] = 'R' + \
                            str(exGrammarIndex)

            # 加入shift
            for input, destination in state_transform.items():
                if input in TERMINATOR:
                    if state_index not in self.action:
                        self.action[state_index] = dict()
                    # 检查这一格是否已经有项目了（说明冲突）
                    if input in self.action[state_index]:
                        self.isLR1 = False
                    self.action[state_index][input] = 'S' + str(destination)

        ...
