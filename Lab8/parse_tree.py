from Lab8.node import Node


class ParseTree:
    NON_TERMINAL_FILL = "#f68c06"
    TERMINAL_CATEGORY_FILL = "#ccc"
    TERMINAL_LEXEME_FILL = "#f8f8f8"

    def __init__(self, root):
        self.root = root

    def export_as_json(self, kfg):
        all_nodes = []
        non_terminals = []
        categories = []
        lexemes = []
        queue = [self.root]
        while queue:
            next = queue.pop()
            if next.value == "EPSILON":
                lexemes.append(next)
                all_nodes.append(next)
            elif next.value in kfg.non_terminals:
                if next.children:
                    queue.extend(next.children)
                else:
                    queue.append(Node("EPSILON", next))
                all_nodes.append(next)
                non_terminals.append(next)
            else:
                category_node = Node(next.value.category, next.parent)
                lexeme_node = Node(next.value.lexeme, category_node)
                category_node.children = "lexeme"
                categories.append(category_node)
                lexemes.append(lexeme_node)
                all_nodes.append(category_node)
                all_nodes.append(lexeme_node)

        out = open("parse_tree/words.sample0.js", "w+")
        out.write("nodeDataArray = [\n")
        for node in all_nodes[::-1]:
            if node == self.root:
                out.write('{ key: ' + str(all_nodes.index(node)) + ', text: "' + node.value + '", fill: "' + self.NON_TERMINAL_FILL + '", stroke: "#4d90fe"' + ' },\n')
            elif node in non_terminals:
                out.write('{ key: ' + str(all_nodes.index(node)) + ', text: "' + node.value + '", fill: "' + self.NON_TERMINAL_FILL + '", stroke: "#4d90fe", parent: ' + str(all_nodes.index(node.parent)) + ' },\n')
            elif node in categories:
                out.write('{ key: ' + str(all_nodes.index(node)) + ', text: "' + node.value + '", fill: "' + self.TERMINAL_CATEGORY_FILL + '", stroke: "#4d90fe", parent: ' + str(all_nodes.index(node.parent)) + ' },\n')
            elif node in lexemes:
                out.write('{ key: ' + str(all_nodes.index(node)) + ', text: "' + node.value + '", fill: "' + self.TERMINAL_LEXEME_FILL + '", stroke: "#4d90fe", parent: ' + str(all_nodes.index(node.parent)) + ' },\n')
        out.write(']')
        out.close()
