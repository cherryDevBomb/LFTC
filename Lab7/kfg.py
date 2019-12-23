import itertools

from Lab7.utils import difference, union, lists_differ


class KFG:
    def __init__(self):
        self.start = None
        self.terminals = []
        self.non_terminals = []
        self.production_rules = {}
        self.first_sets = None
        self.follow_sets = None
        self.first_for_separate_rules = None
        self.rule_indices = None

    def read(self, filename):
        all_symbols = []
        with open(filename) as input:
            # first line is the start symbol
            self.start = input.readline().strip()

            # next lines are production rules
            line = input.readline().strip()
            while line:
                new_rule = []
                rule_head = None
                while line != "":
                    # start of new rule
                    if not line[0] == "|":
                        rule_head = line
                        self.non_terminals.append(rule_head)
                    # continue building rule
                    else:
                        rhs = line.split(" ")[1:]
                        all_symbols.extend(rhs)
                        new_rule.append(rhs)
                    line = input.readline().strip()

                # reached rule end
                self.production_rules[rule_head] = new_rule
                line = input.readline().strip()

        self.terminals = list(set(all_symbols) - set(self.non_terminals))

    def write(self, filepath):
        out = open(filepath, "w+")

        # first line is the start symbol
        out.write(self.start + "\n")

        # next lines are production rules
        for key, val in self.production_rules.items():
            out.write(key + "\n")
            for part in val:
                out.write("| " + " ".join(part) + "\n")
            out.write("\n")

    def export_as_json(self):
        out = open("grammar_tree/sample0.js", "w+")

        # derived children
        out.write("derived_children = {\n")
        for derivation in self.production_rules.values():
            for rule in derivation:
                out.write('\t"' + ' '.join(rule) + '": [\n')
                for part in rule:
                    is_terminal = "true" if part in self.terminals else "false"
                    out.write('\t\t{ "name": "' + part + '", "isTerminal": ' + is_terminal + ' },\n')
                out.write('\t],\n')
        out.write('}\n\n')

        # derivations
        out.write("derivations = {\n")
        for key, values in self.production_rules.items():
            out.write('\t"' + key + '": [\n')
            for derivation in values:
                out.write('\t\t\t{ "name": "' + ' '.join(derivation) + '" },\n')
            out.write('\t\t],\n')
        out.write('}\n\n')

        # root
        out.write("root = {\n")
        out.write('\t"name": "' + self.start + '",\n}')

    def is_regular(self):
        left_flag = None
        right_flag = None
        for rule_list in self.production_rules.values():
            for rule in rule_list:
                if len(rule) > 1:
                    rhs_number_of_non_terminals = sum(1 for elem in rule if elem in self.non_terminals)
                    # more than one non-terminal in the right hand side of rule
                    if rhs_number_of_non_terminals > 1:
                        return False
                    else:
                        rhs_non_terminal = next((elem for elem in rule if elem in self.non_terminals), None)
                        if rhs_non_terminal is None:
                            continue
                        position_of_non_terminal = rule.index(rhs_non_terminal)
                        if position_of_non_terminal == 0:
                            left_flag = True
                        elif position_of_non_terminal == len(rule) - 1:
                            right_flag = True
                        # non-terminal in the middle of rule
                        else:
                            return False
                    # non-terminals are placed in different sides of rules
                    if left_flag and right_flag:
                        return False

        return True

    def compute_first_sets(self):
        first_sets = {}
        first_for_separate_rules = {}

        for symbol in self.terminals:
            first_sets[symbol] = [symbol]
        first_sets["EPSILON"] = ["EPSILON"]
        first_sets[None] = None

        for symbol in self.non_terminals:
            first_sets[symbol] = []

        has_new_change = True
        while has_new_change:
            has_new_change = False
            # iterate over production rules (head_of_rule -> beta)
            for head_of_rule in self.production_rules.keys():
                for beta in self.production_rules[head_of_rule]:
                    if all(symbol in self.terminals or symbol in self.non_terminals for symbol in beta):
                        rhs = difference(first_sets[beta[0]], ["EPSILON"])
                        i = 0
                        while "EPSILON" in first_sets[beta[i]] and i < len(beta)-1:
                            rhs = union(rhs, difference([beta[i+1]], ["EPSILON"]))
                            i += 1
                        k = len(beta)-1
                        if i == k and "EPSILON" in first_sets[beta[k]]:
                            rhs = union(rhs, ["EPSILON"])
                        # save value of FIRST(beta)
                        first_for_separate_rules[str(beta)] = rhs
                        # compute new value of FIRST(head_of_rule) and update if needed
                        new_first_set = union(first_sets[head_of_rule], rhs)
                        if lists_differ(first_sets[head_of_rule], new_first_set):
                            first_sets[head_of_rule] = new_first_set
                            has_new_change = True

        self.first_for_separate_rules = first_for_separate_rules
        self.first_sets = first_sets
        return first_sets

    def compute_follow_sets(self):
        follow_sets = {}

        for symbol in self.non_terminals:
            follow_sets[symbol] = []
        follow_sets[self.start] = [None]

        has_new_change = True
        while has_new_change:
            has_new_change = False
            # iterate over production rules (head_of_rule -> beta)
            for head_of_rule in self.production_rules.keys():
                for beta in self.production_rules[head_of_rule]:
                    trailer = follow_sets[head_of_rule]
                    for i in range(len(beta)-1, -1, -1):
                        if beta[i] in self.non_terminals:
                            new_follow_sets = union(follow_sets[beta[i]], trailer)
                            if lists_differ(follow_sets[beta[i]], new_follow_sets):
                                follow_sets[beta[i]] = new_follow_sets
                                has_new_change = True
                            if "EPSILON" in self.first_sets[beta[i]]:
                                trailer = union(trailer, difference(self.first_sets[beta[i]], ["EPSILON"]))
                            else:
                                trailer = self.first_sets[beta[i]]
                        else:
                            trailer = self.first_sets[beta[i]]

        return follow_sets

    def is_LL1(self):
        for non_terminal in self.non_terminals:
            rules = self.production_rules[non_terminal]
            if len(rules) > 1:
                for i in range(len(rules) - 1):
                    for j in range(i + 1, len(rules) - 1):
                        if any(elem in self.first_plus(non_terminal, rules[i]) for elem in self.first_plus(non_terminal, rules[j])):
                            return False
        return True

    def first_plus(self, non_terminal, beta):
        if "EPSILON" not in self.first_for_separate_rules[str(beta)]:
            return self.first_for_separate_rules[str(beta)]
        else:
            return union(self.first_for_separate_rules[str(beta)], self.follow_sets[non_terminal])

    def compute_rule_indices(self):
        rule_indices = {}
        index = 1
        for non_terminal in self.production_rules.keys():
            for rule in self.production_rules[non_terminal]:
                rule_indices[index] = (non_terminal, rule)
                index += 1
        self.rule_indices = rule_indices

    def eliminate_left_recursion(self):
        for i in range(0, len(self.non_terminals)):
            current_nt_rules = self.production_rules[self.non_terminals[i]]
            for j in range(0, i):
                for rhs in current_nt_rules:
                    # if there is a production Ai -> Aj a, replace it with productions that expand Aj
                    if rhs[0] == self.non_terminals[j]:
                        expansions = []
                        for p in self.production_rules[self.non_terminals[j]]:
                            expansions.append(p + rhs[1:])
                        index = current_nt_rules.index(rhs)
                        current_nt_rules[index:index+1] = expansions
                        list(itertools.chain.from_iterable(current_nt_rules))

            # check if there is any direct left recursion
            has_direct_left_recursion = False
            for rhs in current_nt_rules:
                if rhs[0] == self.non_terminals[i]:
                    has_direct_left_recursion = True
                    break

            # rewrite the productions to eliminate any direct left recursion
            if has_direct_left_recursion:
                new_non_terminal = self.non_terminals[i] + "^"
                rewritten = []
                new_non_terminal_rules = []
                for rhs in current_nt_rules:
                    if rhs[0] == self.non_terminals[i]:
                        new_non_terminal_rules.append(rhs[1:] + [new_non_terminal])
                    elif all(symbol != self.non_terminals[i] for symbol in rhs):
                        rewritten.append(rhs + [new_non_terminal])
                new_non_terminal_rules.append(["EPSILON"])

                self.production_rules[self.non_terminals[i]] = rewritten
                self.non_terminals.append(new_non_terminal)
                self.production_rules[new_non_terminal] = new_non_terminal_rules


if __name__ == "__main__":
    # to test FIRST and FOLLOW sets:
    kfg = KFG()
    kfg.read("input/input_kfg9.txt")

    kfg.first_sets = kfg.compute_first_sets()
    print("First sets are: " + str(kfg.first_sets))
    kfg.follow_sets = kfg.compute_follow_sets()
    print("Follow sets are: " + str(kfg.follow_sets))
    print("KFG is LL(1)") if kfg.is_LL1() else print("KFG is not LL(1)")

    # to test elimination of left recursion
    # kfg = KFG()
    # kfg.read("input/input8.txt")
    # kfg.eliminate_left_recursion()
    # kfg.write("output/output8.txt")
