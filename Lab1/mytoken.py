from enum import Enum


class Token:
    def __init__(self, t_type, content, line_number):
        self.type = t_type
        self.content = content
        self.line_number = line_number

    def __repr__(self):
        return self.content + "(" + str(self.type.name) + ")"


class TokenType(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    OPERATOR = 3
    INTEGER = 4
    FLOAT = 5
    UNKNOWN = 6