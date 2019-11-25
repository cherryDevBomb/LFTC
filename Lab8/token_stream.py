from Lab8.my_token import MyToken


class TokenStream:

    def __init__(self):
        self.tokens = []
        self.index = -1

    def from_file(self, filename):
        with open(filename) as input:
            line = input.readline()
            while line:
                line = line.strip().split(" ")
                token = MyToken(line[0], line[1])
                self.tokens.append(token)
                line = input.readline()

    def next_word(self):
        self.index += 1
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None

    def push_front(self, number):
        self.index -= number

