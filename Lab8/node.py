
class Node:

    def __init__(self, value, parent):
        self.value = value
        self.children = None
        self.parent = parent
        self.derivation_index = 0

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
