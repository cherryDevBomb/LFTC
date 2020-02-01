from Lab7.cfg import CFG
from Lab8.token_stream import TokenStream


class LL1:

    def __init__(self, cfg):
        cfg.first_sets = cfg.compute_first_sets()
        cfg.follow_sets = cfg.compute_follow_sets()
        if not cfg.is_LL1():
            raise ValueError("The grammar should be LL1")
        self.cfg = cfg

    def parse(self, token_stream):
        table = self.create_table()
        self.print_table(table)

        stack = [None, cfg.start]
        word = token_stream.next_word()
        focus = cfg.start
        print("Current word is: " + str(word))

        while True:
            if focus is None and word is None:
                # successfully parsed input
                return True
            elif focus in cfg.terminals or focus is None:
                if focus == word.category:
                    # focus matches word
                    stack.pop()
                    word = token_stream.next_word()
                    print("Current word is: " + str(word))
                else:
                    print("Input cannot be parsed.")
                    return False
            else:
                # focus is a non-terminal
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

        for non_terminal in self.cfg.non_terminals:
            table[non_terminal] = {}
            for terminal in self.cfg.terminals:
                if terminal != "EPSILON":
                    table[non_terminal][terminal] = "err"
            table[non_terminal][None] = "err"

            for beta in self.cfg.production_rules[non_terminal]:
                for terminal_w in self.cfg.first_plus(non_terminal, beta):
                    if terminal_w != "EPSILON":
                        table[non_terminal][terminal_w] = beta
                if None in self.cfg.first_plus(non_terminal, beta):
                    table[non_terminal][None] = beta

        return table

    def print_table(self, table):
        print("LL(1) table:")
        for non_terminal, pairs in table.items():
            for terminal, rule in pairs.items():
                print("table[" + non_terminal + ", " + str(terminal) + "] = " + str(rule))
        print()


if __name__ == "__main__":
    cfg = CFG()
    cfg.read("input/input_cfg9.txt")

    token_str = TokenStream()
    token_str.from_file("input/input9.txt")

    ll_1_parser = LL1(cfg)
    ll_1_parser.parse(token_str)