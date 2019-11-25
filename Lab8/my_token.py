
class MyToken:

    def __init__(self, lexeme, category):
        self.lexeme = lexeme
        self.category = category

    def __str__(self):
        return self.lexeme + " " + self.category
