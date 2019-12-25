from Lab2.edge import Edge
from Lab2.node import *


class FA:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.edge_labels = []

    def read_fa(self, filepath):
        with open(filepath) as input:
            # first line is number of nodes
            number_of_nodes = int(input.readline().strip())
            for i in range (0, number_of_nodes):
                self.nodes.append(Node(i))

            # second line is number of edge labels
            number_of_edge_labels = int(input.readline().strip())

            # third line is list of edge labels
            list_of_edge_labels = input.readline().strip().split()
            self.edge_labels = list_of_edge_labels

            # fourth line is number of edges
            number_of_edges = int(input.readline().strip())

            # next lines are edges
            for i in range (0, number_of_edges):
                line = input.readline().strip().split()
                e = Edge(line[0], line[1], line[2])
                self.edges.append(e)

            # next line is start node
            start_node = int(input.readline().strip())
            self.nodes[start_node].is_start = True

            # next line is number of end nodes
            number_of_end_nodes = int(input.readline().strip())

            # next line is end nodes
            end_nodes = input.readline().strip().split()
            for n in end_nodes:
                self.nodes[int(n)].is_end = True

    def write_fa(self, filepath):
        out = open(filepath, "w+")

        # first line is number of nodes
        number_of_nodes = len(self.nodes)
        out.write(str(number_of_nodes) + "\n")

        # second line is number of edge labels
        number_of_edge_labels = len(set(map(lambda x: x.label, self.edges)))
        out.write(str(number_of_edge_labels) + "\n")

        # third line is list of edge labels
        list_of_edge_labels = sorted(set(map(lambda x: x.label, self.edges)))
        out.write(" ".join(list_of_edge_labels) + "\n")

        # fourth line is number of edges
        number_of_edges = len(self.edges)
        out.write(str(number_of_edges) + "\n")

        # next lines are edges
        for edge in self.edges:
            out.write(str(edge) + "\n")

        # next line is start node
        node = self.get_start_node()
        out.write(str(node.id) + "\n")

        # next line is number of end nodes
        end_nodes = []
        for node in self.nodes:
            if node.is_end:
                end_nodes.append(node)
        number_of_end_nodes = len(end_nodes)
        out.write(str(number_of_end_nodes) + "\n")

        # next line is end nodes
        end_nodes_str = list(map(lambda x: str(x.id), end_nodes))
        out.write(" ".join(end_nodes_str) + "\n")

    def get_start_node(self):
        for node in self.nodes:
            if node.is_start:
                return node

    def get_end_nodes(self):
        end_nodes = []
        for node in self.nodes:
            if node.is_end:
                end_nodes.append(node)
        return end_nodes

    def get_node_by_id(self, id_str):
        for node in self.nodes:
            if str(node.id)  == id_str:
                return node

    def accept_string(self, string):
        node = self.get_start_node()
        index = 0
        for char in string:
            found = False
            for edge in self.edges:
                if int(edge.start_node) == node.id and edge.label == char:
                    node = self.nodes[int(edge.end_node)]
                    found = True
                    if node.is_end and index == len(string)-1:
                        return True
            if not found:
                return False
            index += 1
        return True

    def export_nodes_as_json(self):
        nodes_list = []
        for node in self.nodes:
            node_data = "{ id: " + str(node.id) + ", "
            node_data += "label: 's" + str(node.id) + "', "
            node_data += "color: "
            if node.is_start:
                node_data += "'#ff5530'"
            elif node.is_end:
                node_data += "'#7BE141'"
            else:
                node_data += "'#98caf9'"
            node_data += " }"
            nodes_list.append(node_data)

        nodes_json = "nodes_json = [\n" + ",\n".join(nodes_list) + "\n]\n"
        return nodes_json

    def export_edges_as_json(self):
        edges_list = []
        for edge in self.edges:
            edge_data = "{ from: " + edge.start_node + ", "
            edge_data += "to: " + edge.end_node + ", "
            edge_data += "arrows: 'to', "
            edge_data += "color: { color: " + "'#008fe6'" + " }, "
            edge_data += "label: '" + edge.label + "', font: { align: 'middle' }  }"
            edges_list.append(edge_data)

        edges_json = "edges_json = [\n" + ",\n".join(edges_list) + "\n]\n"
        return edges_json

    def export_as_json(self):
        json_nodes = self.export_nodes_as_json()
        json_edges = self.export_edges_as_json()
        with open("finite_automata/data.js") as content_js:
            content = "".join(content_js.readlines())

        with open("finite_automata/graph.js", "w+") as output:
            output.write(json_nodes)
            output.write(json_edges)
            output.write(content)


if __name__ == "__main__":
    fa = FA()
    fa.read_fa("input/input3.txt")
    fa.write_fa("output/output3.txt")

    # export as json
    fa.export_as_json()

    # test accept string
    print(fa.accept_string("abc"))
    print(fa.accept_string("abacc"))
    print(fa.accept_string("aca"))
