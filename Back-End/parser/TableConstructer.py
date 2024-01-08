import json
from Grammar import NON_TERMINATOR


class TableConstructer:
    def __init__(self, url):
        with open('Back-End/parser/temp/specfamily.json') as file:
            self.specfamily = json.load(file)
        self.table = {"ACTION": dict(), "GOTO": dict()}

    def run(self):
        self.construct_goto()
        self.construct_action()

    def construct_goto(self):

        for state in self.specfamily:

            state_index = state["state"]
            state_transform = state["transform"]
            for key, value in state_transform.items():
                if key in NON_TERMINATOR:
                    print(key, value)
                    if key not in self.table["GOTO"]:
                        self.table["GOTO"][key] = dict()
                    self.table["GOTO"][key][state_index] = value

    def construct_action(self):
        pass


def main():
    table_constructer = TableConstructer(
        'Back-End/parser/temp/specfamily.json')
    table_constructer.run()
    print(table_constructer.table)


main()
