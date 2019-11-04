import re
from Lab1.mytoken import Token
from Lab1.mytoken import TokenType


class Scanner:
    tokens = []

    keywords = [
        "VAR",
        "PROCEDURE",
        "BEGIN",
        "END",
        "WHILE",
        "DO",
        "CALL"
    ]

    operators = {
        "PLUS": "+",
        "MINUS": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "ASSIGN": ":=",
        "GREATER": ">",
        "LESS": "<",
        "GREATEREQ": ">=",
        "LESSEQ": "<=",
        "EQ": "==",
        "NOT": "!"
    }

    def __init__(self, filename):
        self.filename = filename

        self.comment_pattern = "//.*"
        self.identifier_pattern = "^[a-zA-Z_]\w*"
        self.int_pattern = "^[1-9]{1}[0-9]*|^0"
        self.float_pattern = "^[0-9]+\.[0-9]+"
        self.unknown_pattern = "^\.|^,|^;"
        self.operator_pattern = "^\+|^-|^\*|^\/|^>=|^<=|^==|^=|^>|^<|^\!|^:="

        keyword_pattern = "^"
        for key in Scanner.keywords:
            keyword_pattern += key
            keyword_pattern += "|^"
        self.keyword_pattern = keyword_pattern[:-2]

    def scan(self):
        line_nr = 1
        with open(self.filename) as input:
            line = input.readline()
            while line:
                # match comment
                if re.search(self.comment_pattern, line):
                    line = line.split("//")[0]

                line = line.strip()
                if len(line) > 0:
                    line_tokens = self.tokenize(line)
                    self.tokens.append(line_tokens)

                # go to next line
                line = input.readline()
                line_nr += 1

    def tokenize(self, line):
        line_tokens = []
        while len(line) > 0:
            is_keyword = re.match(self.keyword_pattern, line)
            is_identifier = re.match(self.identifier_pattern, line)
            is_operator = re.match(self.operator_pattern, line)
            is_float = re.match(self.float_pattern, line)
            is_int = re.match(self.int_pattern, line)
            is_unknown = re.match(self.unknown_pattern, line)

            if is_keyword:
                content = is_keyword.group()
                line_tokens.append(Token(TokenType.KEYWORD, content))
                line = line[len(content):].strip()
            elif is_identifier:
                content = is_identifier.group()
                line_tokens.append(Token(TokenType.IDENTIFIER, content))
                line = line[len(content):].strip()
            elif is_operator:
                content = is_operator.group()
                line_tokens.append( Token(TokenType.OPERATOR, content))
                line = line[len(content):].strip()
            elif is_float:
                content = is_float.group()
                line_tokens.append(Token(TokenType.FLOAT, content))
                line = line[len(content):].strip()
            elif is_int:
                content = is_int.group()
                line_tokens.append(Token(TokenType.INTEGER, content))
                line = line[len(content):].strip()
            elif is_unknown:
                content = is_unknown.group()
                line_tokens.append(Token(TokenType.UNKNOWN, content))
                line = line[len(content):].strip()

        return line_tokens

    def print_output_to_file(self):
        out = open("output.txt", "w+")
        for line in self.tokens:
            for token in line:
                out.write(str(token) + " ")
            out.write("\n")

    def print_output(self):
        print(self.tokens)
        for line in self.tokens:
            for token in line:
                print(token, end=" ")
            print()


if __name__ == "__main__":
    scanner = Scanner("input.txt")
    scanner.scan()
    scanner.print_output_to_file()
    scanner.print_output()
