class Node:
    def __init__(self, id):
        self.id = id
        self.is_start = False
        self.is_end = False

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, start_node, end_node, label):
        self.start_node = start_node
        self.end_node = end_node
        self.label = label

    def __str__(self):
        return self.start_node + " " + self.end_node + " " + self.label
