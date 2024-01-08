from Grammar import NON_TERMINATOR


"""
分析表的例子它就像下面这样

    "ACTION":{"0":{
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
    }}


    "GOTO":{
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

    

"""


class AnalysisTable:

    def __init__(self, specFamily):
        self.specFamily = specFamily
        self.action = dict()
        self.goto = dict()

    def construct_goto(self):
        for specFamilyItem in self.specFamily.content:
            state_index = specFamilyItem.state
            state_transform = specFamilyItem.transfrom
            for key, values in state_transform.items():
                if key in NON_TERMINATOR:
                    if key not in self.goto:
                        self.goto[key] = dict()
                    self.goto[key][state_index] = values
        ...

    def construct_action(self):
        ...
