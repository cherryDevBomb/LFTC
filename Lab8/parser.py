from Lab7.cfg import CFG
from Lab8.parse_tree import ParseTree
from Lab8.node import Node
from Lab8.token_stream import TokenStream


class Parser:

    def parse(self, token_stream, cfg):
        root = Node(cfg.start, None)
        focus = root
        stack = [None]
        word = token_stream.next_word()
        while True:
            if focus and (focus.value in cfg.non_terminals):
                # pick next rule to expand focus (A -> beta_1, ... , beta_n)
                next_rule = cfg.production_rules[focus.value][focus.derivation_index]
                print("Expanding focus {} with rule {}: {}".format(focus.value, focus.derivation_index, next_rule))
                focus.derivation_index += 1
                # check for epsilon
                if next_rule == ["EPSILON"]:
                    focus = stack.pop()
                    continue
                # build nodes for (beta_1, ... , beta_n) as children of focus
                focus.children = [Node(beta, focus) for beta in next_rule]
                # push (beta_n, ... , beta_2) onto the stack
                if len(next_rule) > 1:
                    for beta in focus.children[-1:0:-1]:
                        stack.append(beta)
                # beta_1 is the new focus
                focus = focus.children[0]
            elif word and focus and (word.category == focus.value):
                # make value save category as well as lexeme
                focus.value = word

                print("Match {}".format(word.category))
                word = token_stream.next_word()
                focus = stack.pop()
            else:
                if word is None and focus is None:
                    # accept input
                    return ParseTree(root)
                else:
                    # backtracking
                    while focus and (focus.value not in cfg.non_terminals or focus.derivation_index > len(cfg.production_rules[focus.value]) - 1):
                        print("BACKTRACKING: return to parent {}".format(focus.parent))
                        parent = focus.parent
                        # input contains syntax error
                        if parent is None:
                            print("Input cannot be parsed.")
                            return False
                        # clear children from stack
                        for i in range(len(parent.children[parent.children.index(focus):]) - 1):
                            stack.pop()
                        # rewind input stream
                        to_revert = self.get_matched_length(parent.children[:parent.children.index(focus)])
                        token_stream.push_front(to_revert)
                        # reset children and set focus to parent
                        parent.children = None
                        focus = parent

    def get_matched_length(self, children):
        nr = 0
        for child in children:
            if child.children is None:
                nr += 1
            else:
                nr += self.get_matched_length(child.children)
        return nr


if __name__=="__main__":
    cfg = CFG()
    cfg.read("input/input_cfg10.txt")

    token_str = TokenStream()
    token_str.from_file("input/input10.txt")

    parser = Parser()
    tree = parser.parse(token_str, cfg)
    tree.export_as_json(cfg)