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
