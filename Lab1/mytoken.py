from enum import Enum


class Token:
    def __init__(self, t_type, content):
        self.type = t_type
        self.content = content

    def __repr__(self):
        return self.content + "(" + str(self.type.name) + ")"


class TokenType(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    OPERATOR = 3
    INTEGER = 4
    FLOAT = 5
    UNKNOWN = 6
    COMMENT = 7
