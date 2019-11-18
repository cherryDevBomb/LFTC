
class KFG:
    def __init__(self):
        self.start = None
        self.terminals = []
        self.non_terminals = []
        self.production_rules = {}

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

    def write(self):
        out = open("output7.txt", "w+")

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


if __name__ == "__main__":
    kfg = KFG()
    kfg.read("input8.txt")
    kfg.write()
    kfg.export_as_json()
    print(kfg.production_rules)

    print("KFG is regular: " + str(kfg.is_regular()))
