
class LR1Item:

    def __init__(self, production, stacktop_position, lookahead):
        self.production = production
        self.stacktop_position = stacktop_position
        self.lookahead = lookahead

    def __eq__(self, other):
        return self.production == other.production and self.stacktop_position == other.stacktop_position and self.lookahead == other.lookahead

    def __hash__(self):
        return hash(self.production[0]) + hash(str(self.production[1])) + hash(self.stacktop_position) + hash(self.lookahead)

    def __str__(self):
        return "[" + self.production[0] + ' -> ' + ' '.join(self.production[1][:self.stacktop_position]) + " * " + ' '.join(self.production[1][self.stacktop_position:]) + ', ' + str(self.lookahead) + ']'

    def __repr__(self):
        return self.production[0] + ' -> ' + ' '.join(self.production[1][:self.stacktop_position]) + " * " + ' '.join(self.production[1][self.stacktop_position:]) + ', ' + str(self.lookahead) + ']'
