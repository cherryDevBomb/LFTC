from Lab7.kfg import KFG
from Lab8.token_stream import TokenStream


class LL1:

    def __init__(self, kfg):
        kfg.first_sets = kfg.compute_first_sets()
        kfg.follow_sets = kfg.compute_follow_sets()
        if not kfg.is_LL1():
            raise ValueError("The grammar should be LL1")
        self.kfg = kfg

    def parse(self, token_stream):
        table = self.create_table()
        self.print_table(table)

        stack = [None, kfg.start]
        word = token_stream.next_word()
        focus = kfg.start
        print("Current word is: " + str(word))

        while True:
            # successfully parsed input
            if focus is None and word is None:
                return True
            elif focus in kfg.terminals or focus is None:
                # focus matches word
                if focus == word.category:
                    stack.pop()
                    word = token_stream.next_word()
                    print("Current word is: " + str(word))
                else:
                    print("Input cannot be parsed.")
                    return False
            # focus is a non-terminal
            else:
                w = word.category if word is not None else None
                if table[focus][w] != "err":
                    beta = table[focus][w]
                    print("Rule: " + str(focus) + " -> " + str(beta), end="; ")
                    stack.pop()
                    for symbol in beta[::-1]:
                        if symbol != "EPSILON":
                            stack.append(symbol)
                        print("Stack: " + str(stack))
                else:
                    print("Input cannot be parsed.")
                    return False
            focus = stack[-1]



    def create_table(self):
        table = {}

        for non_terminal in self.kfg.non_terminals:
            table[non_terminal] = {}
            for terminal in self.kfg.terminals:
                if terminal != "EPSILON":
                    table[non_terminal][terminal] = "err"
            table[non_terminal][None] = "err"

            for beta in self.kfg.production_rules[non_terminal]:
                for terminal_w in self.kfg.first_plus(non_terminal, beta):
                    if terminal_w != "EPSILON":
                        table[non_terminal][terminal_w] = beta
                if None in self.kfg.first_plus(non_terminal, beta):
                    table[non_terminal][None] = beta

        return table

    def print_table(self, table):
        print("LL(1) table:")
        for non_terminal, pairs in table.items():
            for terminal, rule in pairs.items():
                print("table[" + non_terminal + ", " + str(terminal) + "] = " + str(rule))
        print()


if __name__ == "__main__":
    kfg = KFG()
    kfg.read("input/input_kfg9.txt")

    token_str = TokenStream()
    token_str.from_file("input/input9.txt")

    ll_1_parser = LL1(kfg)
    ll_1_parser.parse(token_str)