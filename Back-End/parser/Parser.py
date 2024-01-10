from utils import find_first, find_follow
import json

class Parser:
    def __init__(self, AnalysisTable, json_path, token_to_terminator_bb, terminator_, non_terminator_, grammar):
        self.token_to_terminator_bb = token_to_terminator_bb
        self.analysetable = AnalysisTable
        self.input = self.json_to_str(json_path)
        self.non_terminator_in = non_terminator_
        self.terminator_in = terminator_
        self.state_stack = [0]
        self.symbol_stack = []
        self.grammar = grammar
        self.first = {non_term: set() for non_term in non_terminator_}
        self.follow = {non_term: set() for non_term in non_terminator_} 

    def json_to_str(self, json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        input = ""

        for _, value in data.items():
            print(value[0])
            input += self.token_to_terminator_bb(value[0])
            input = input + " "
        return input

    def compute_fir_fol(self):
        for non_terminator in self.non_terminator_in:
            self.first[non_terminator] = find_first([non_terminator], self.non_terminator_in, self.grammar, self.terminator_in)

        self.follow = find_follow(self.non_terminator_in[0])

    def analyse(self, recovery):
        action_table = self.analysetable.action
        goto_table = self.analysetable.goto
        input_buffer = self.input.split() + ['$']

        print("{:<50} {:<50} {:<50} {:<50}".format("State Stack", "Symbol Stack", "Input", "Action"))

        while True:
            current_state = self.state_stack[-1]
            current_symbol = input_buffer[0]
            action_entry = action_table.get(current_state)
            # print(current_state)
            if action_entry is not None:
                action = action_entry.get(current_symbol)
                # print(current_symbol)
                if action is not None:
                    state_stack_str = str(self.state_stack)
                    symbol_stack_str = str(self.symbol_stack)
                    input_buffer_str = str(input_buffer)
                    action_str = str(action)

                    print("{:<50} {:<50} {:<50} {:<50}".format(state_stack_str, symbol_stack_str, input_buffer_str,
                                                            action_str))

                    if action[0] == 'S':
                        # 移入操作，将状态和符号入栈
                        new_state = action[1:]
                        self.state_stack.append(int(new_state))
                        self.symbol_stack.append(current_symbol)
                        input_buffer.pop(0)
                    elif action[0] == 'R':
                        # 规约操作，弹出相应数量的状态和符号，进行Goto操作
                        index = int(action[1:])
                        lhs = self.analysetable.specFamily.exgrammar[index][1]
                        rhs = self.analysetable.specFamily.exgrammar[index][2]
                        num_to_pop = len(rhs)
                        for _ in range(num_to_pop):
                            if rhs != ['ε']:
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
                    print("Error: Invalid Input. Attempting error recovery.")

                    # 错误恢复：从栈顶开始回退，直到找到状态 s，该状态具有预先确定的非终结符 A 的转移
                    while len(self.state_stack) > 0:
                        top_state = self.state_stack[-1]
                        if goto_table.get(recovery).get(top_state) is not None:
                            break
                        self.state_stack.pop()
                    # 丢弃输入符号，直至找到符号 a，它可以合法地跟随 A
                    while len(input_buffer) > 0 and input_buffer[0] not in self.follow.get(recovery) and input_buffer[0] != '$':
                        input_buffer.pop(0)
                    
                    if input_buffer[0] == '$' or input_buffer[0] == '.':
                        print("No input symbol can be found for the error to be successfully recovered!")
                        break
                    # 恢复正常分析：将 A 和 goto[s, A] 推入栈中

                    self.symbol_stack.append(recovery)
                    new_state = goto_table.get(recovery).get(top_state)
                    self.state_stack.append(int(new_state))
            else:
                print("Error: Invalid Input")
                break


