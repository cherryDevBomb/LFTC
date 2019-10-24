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

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


class Edge:
    def __init__(self, start_node, end_node, label):
        self.start_node = start_node
        self.end_node = end_node
        self.label = label

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.start_node == other.start_node and self.end_node == other.end_node and self.label == other.label

    def __hash__(self):
        return hash(self.start_node) + hash(self.end_node) + hash(self.label)

    def __str__(self):
        return self.start_node + " " + self.end_node + " " + self.label
