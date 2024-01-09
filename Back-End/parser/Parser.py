from .AnalysisTable import AnalysisTable
from pathlib import Path
import json


class Parser:
    def __init__(self, AnalysisTable, json_path, token_to_terminator_bb):
        self.token_to_terminator_bb = token_to_terminator_bb
        self.analysetable = AnalysisTable
        self.input = self.json_to_str(json_path)
        self.state_stack = [0]
        self.symbol_stack = []

    def json_to_str(self, json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        input = ""

        for _, value in data.items():
            input += self.token_to_terminator_bb(value[0])

        return input

    def analyse(self):
        action_table = self.analysetable.action
        goto_table = self.analysetable.goto
        input_buffer = list(self.input) + ['$']

        print("{:<20} {:<20} {:<20} {:<20}".format("State Stack", "Symbol Stack", "Input", "Action"))

        while True:
            current_state = self.state_stack[-1]
            current_symbol = input_buffer[0]
            action_entry = action_table.get(current_state)

            if action_entry is not None:
                action = action_entry.get(current_symbol)

                if action is not None:
                    state_stack_str = str(self.state_stack)
                    symbol_stack_str = str(self.symbol_stack)
                    input_buffer_str = str(input_buffer)
                    action_str = str(action)

                    print("{:<20} {:<20} {:<20} {:<20}".format(state_stack_str, symbol_stack_str, input_buffer_str,
                                                               action_str))

                    if action[0] == 'S':
                        # 移入操作，将状态和符号入栈
                        new_state = action[1]
                        self.state_stack.append(int(new_state))
                        self.symbol_stack.append(current_symbol)
                        input_buffer.pop(0)
                    elif action[0] == 'R':
                        # 规约操作，弹出相应数量的状态和符号，进行Goto操作
                        index = int(action[1])
                        lhs = self.analysetable.specFamily.exgrammar[index][1]
                        rhs = self.analysetable.specFamily.exgrammar[index][2]
                        num_to_pop = len(rhs)

                        for _ in range(num_to_pop):
                            self.symbol_stack.pop(-1)
                            self.state_stack.pop(-1)

                        self.symbol_stack.append(lhs)
                        current_state = self.state_stack[-1]
                        new_state = goto_table.get(lhs).get(current_state)
                        self.state_stack.append(int(new_state))
                    elif action == "ACC":
                        print("Input Accepted!")
                        break
                else:
                    print("Error: Invalid Input")
                    break
            else:
                print("Error: Invalid Input")
                break
