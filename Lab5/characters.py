class Characters:
    
    def __init__(self, src_file):
        self.position = -1
        self.content = ""
        with open(src_file, "r") as f:
            self.content = f.read()

    def next_char(self):
        if self.has_next():
            self.position += 1
            return self.content[self.position]
        return None

    def rollback(self):
        self.position -= 1

    def has_next(self):
        return self.position != len(self.content) - 1
