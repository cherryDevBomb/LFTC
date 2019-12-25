from Lab12.lr1_item import LR1Item
from Lab7.kfg import KFG
from Lab7.utils import union


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
    kfg.read("input/input_kfg11.txt")

    table_generator = TableGenerator(kfg)
    start_s = [LR1Item(kfg.rule_indices[1], 0, None)]
    for item in table_generator.closure(start_s):
        print(item)
