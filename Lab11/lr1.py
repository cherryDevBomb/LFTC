from Lab11.table import LRTable
from Lab7.kfg import KFG
from Lab8.token_stream import TokenStream


class LR1:

    def __init__(self, kfg, table):
        self.kfg = kfg
        self.table = table
        kfg.compute_rule_indices()

    def parse(self, token_stream):
        stack = [0]
        word = token_stream.next_word().category

        while True:
            state = stack[-1]
            print('State: ' + str(state) + '; Word: ' + str(word) + '; Stack: ' + str(stack) + '; ', end='')
            # if Action[state, word] = "reduce A -> beta"
            if self.table.action[word][state][0] == 'r':
                print('Action: ' + self.table.action[word][state])
                rule_index = int(self.table.action[word][state][1:])
                production = self.kfg.rule_indices[rule_index]
                for i in range(2 * len(production[1])):
                    stack.pop()
                state = stack[-1]
                stack.append(production[0])
                stack.append(int(self.table.goto[production[0]][state]))
            # if Action[state, word] = "shift si"
            elif self.table.action[word][state][0] == 's':
                print('Action: ' + self.table.action[word][state])
                stack.append(word)
                stack.append(int(self.table.action[word][state][1:]))
                word = token_stream.next_word()
                word = word.category if word is not None else None
            # if Action[state, word] = "accept"
            elif self.table.action[word][state] == 'acc':
                print('Action: ' + self.table.action[word][state])
                print("Success")
                return True
            else:
                print("\nThis input cannot be parsed")
                return False


if __name__ == "__main__":
    kfg = KFG()
    kfg.read("input/input_kfg11.txt")

    table = LRTable()
    table.from_file("input/table.txt")

    token_str = TokenStream()
    token_str.from_file("input/input11.txt")

    lr_1_parser = LR1(kfg, table)
    lr_1_parser.parse(token_str)
