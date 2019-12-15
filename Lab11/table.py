
class LRTable:

    def __init__(self):
        self.action = {}
        self.goto = {}

    def from_file(self, filename):
        with open(filename) as input:
            line = input.readline().strip()
            while line != "":
                # save table values for Action where state is the index in the column list
                symbol = line if line != 'None' else None
                column = input.readline().strip().split(" ")
                self.action[symbol] = column
                line = input.readline().strip()

            line = input.readline().strip()
            while line:
                # save table values for Goto where state is the index in the column list
                symbol = line if line != 'None' else None
                column = input.readline().strip().split(" ")
                self.goto[symbol] = column
                line = input.readline().strip()
