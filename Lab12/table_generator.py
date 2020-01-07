from Lab11.lr1 import LR1
from Lab11.table import LRTable
from Lab12.lr1_item import LR1Item
from Lab7.kfg import KFG
from Lab7.utils import union
from Lab8.token_stream import TokenStream


class TableGenerator:

    def __init__(self, kfg):
        self.kfg = kfg
        self.kfg.compute_first_sets()
        self.kfg.compute_rule_indices()

    def closure(self, s):
        is_changing = True
        while is_changing:
            is_changing = False
            # for each item "A -> beta * C delta, a"
            for item in s:
                if item.stacktop_position < len(item.production[1]):
                    # for each production C -> gamma
                    c = item.production[1][item.stacktop_position]
                    # rhs_of_c is "delta a"
                    rhs_of_c = item.production[1][item.stacktop_position + 1:]
                    rhs_of_c.append(item.lookahead)
                    if c in self.kfg.non_terminals:
                        for production in self.kfg.production_rules[c]:
                            for b in self.first(rhs_of_c):
                                new_item = LR1Item((c, production), 0, b)
                                if new_item not in s:
                                    is_changing = True
                                    s = union(s, [new_item])

        return list(set(s))

    def goto(self, s, x):
        moved = []
        for i in s:
            if i.stacktop_position < len(i.production[1]):
                if i.production[1][i.stacktop_position] == x:
                    new_item = LR1Item(i.production, i.stacktop_position + 1, i.lookahead)
                    moved = union(moved, [new_item])

        return self.closure(moved)

    def build_cc(self):
        start_s = [LR1Item(self.kfg.rule_indices[1], 0, None)]
        cc0 = table_generator.closure(start_s)
        cc = [cc0]
        processed = []
        changed = True

        while changed:
            changed = False
            for cci in cc:
                if cci not in processed:
                    processed.append(cci)
                    for item in cci:
                        if item.stacktop_position < len(item.production[1]):
                            x = item.production[1][item.stacktop_position]
                            temp = self.goto(cci, x)
                            if temp not in cc:
                                cc.append(temp)
                                changed = True

        return cc

    def fill_tables(self, cc):
        nr_of_states = len(cc)

        # initialize action and goto
        table = LRTable()
        for t in self.kfg.terminals:
            table.action[t] = ['-' for i in range(nr_of_states)]
        table.action[None] = ['-' for i in range(nr_of_states)]
        for nt in self.kfg.non_terminals:
            table.goto[nt] = ['-' for i in range(nr_of_states)]

        # fill tables
        for i in range(nr_of_states):
            for item in cc[i]:
                # item is [A -> beta * c gamma, a] and goto(cci, c) = ccj
                if item.stacktop_position < len(item.production[1]):
                    c = item.production[1][item.stacktop_position]
                    if c in self.kfg.terminals and self.goto(cc[i], c) in cc:
                        ccj = self.goto(cc[i], c)
                        table.action[c][i] = 's' + str(cc.index(ccj))
                elif item.stacktop_position == len(item.production[1]):
                    # item is [S' -> S *, eof] where S' is the goal
                    if item.production[0] == self.kfg.start and item.lookahead is None:
                        table.action[None][i] = 'acc'
                    # item is [A -> beta *, a]
                    else:
                        table.action[item.lookahead][i] = 'r' + str(self.kfg.get_index_of_rule(item.production))

            for nt in self.kfg.non_terminals:
                ccj = self.goto(cc[i], nt)
                if ccj in cc:
                    table.goto[nt][i] = str(cc.index(ccj))

        return table

    def first(self, symbol_set):
        first_set = []
        for symbol in symbol_set:
            to_add = self.kfg.first_sets[symbol] if self.kfg.first_sets[symbol] is not None else [None]
            first_set = union(first_set, to_add)
            if symbol is not "EPSILON":
                break
        return first_set


if __name__ == "__main__":
    kfg = KFG()
    kfg.read("input/input_kfg12.txt")

    table_generator = TableGenerator(kfg)
    start_s = [LR1Item(kfg.rule_indices[1], 0, None)]

    cc = table_generator.build_cc()
    print("Canonical collection:")
    for cci in cc:
        print(cci)
    print()
    table = table_generator.fill_tables(cc)
    table.write_to_file("output/output12.txt")

    token_str = TokenStream()
    token_str.from_file("input/input12.txt")

    lr_1_parser = LR1(kfg, table)
    lr_1_parser.parse(token_str)
