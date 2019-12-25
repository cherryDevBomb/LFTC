from Lab1.mytoken import Token, TokenType
from Lab2.fa import FA
from Lab5.characters import Characters
from Lab5.generate_table import create_scanner_table


class Scanner:

    def __init__(self, table_dictionary):
        self.table_dictionary = table_dictionary
        self.keywords = ['VAR', 'PROCEDURE', 'CALL', 'BEGIN', 'END', 'DO', 'WHILE']
        self.operators = ['!', '*', '+', '-', '/', '=', '<', '>', ':=', '<=', '>=']

    def parse(self, cs):
        tokens = []
        char = ""
        while cs.has_next():
            # skip whitespace
            if char in [' ', '\t', '\n']:
                char = cs.next_char()
            # treat "," and ";" as unknown
            if char in [',', ';', '.']:
                token = Token(TokenType.UNKNOWN, char)
                tokens.append(token)
                char = cs.next_char()

            for type, table in self.table_dictionary.items():
                state = table.start_state
                lexeme = ""
                stack = []
                while state != "err":
                    char = cs.next_char()
                    # break if reached EOF
                    if not char:
                        break

                    lexeme += char
                    if state in table.end_states:
                        stack = []
                    stack.append(state)

                    # get index of symbol class to which the char belongs
                    char_index = -1
                    for symbol_class, values in table.symbol_dict.items():
                        if char in values:
                            char_index = table.symbols.index(symbol_class)
                            break
                    # move to the next state
                    if char_index != -1:
                        state = table.incidence_matrix[state][char_index]
                    # reached error state
                    else:
                        state = "err"

                # clean up final state
                while (state not in table.end_states) and (len(stack) > 0):
                    state = stack.pop()
                    lexeme = lexeme[:-1]
                    cs.rollback()

                # additional check for operators and keywords
                if state in table.end_states:
                    if TokenType(type) == TokenType.OPERATOR:
                        if lexeme not in self.operators:
                            break
                    if TokenType(type) == TokenType.IDENTIFIER:
                        if lexeme in self.keywords:
                            type = 1
                    # create token
                    token = Token(TokenType(type), lexeme)
                    tokens.append(token)
                    break

        return tokens


if __name__ == "__main__":
    # saves each created table to corresponding TokenType index
    table_dictionary = {}

    fa_comment = FA()
    fa_comment.read_fa("input/comment.txt")
    comment_table = create_scanner_table(fa_comment, "output_tables/comment.tab")
    table_dictionary[7] = comment_table 

    fa_float = FA()
    fa_float.read_fa("input/float.txt")
    float_table = create_scanner_table(fa_float, "output_tables/float.tab")
    table_dictionary[5] = float_table

    fa_identifier = FA()
    fa_identifier.read_fa("input/identifier.txt")
    identifier_table = create_scanner_table(fa_identifier, "output_tables/identifier.tab")
    table_dictionary[2] = identifier_table

    fa_integer = FA()
    fa_integer.read_fa("input/integer.txt")
    integer_table = create_scanner_table(fa_integer, "output_tables/integer.tab")
    table_dictionary[4] = integer_table

    fa_operator = FA()
    fa_operator.read_fa("input/operator.txt")
    operator_table = create_scanner_table(fa_operator, "output_tables/operator.tab")
    table_dictionary[3] = operator_table

    # parse program and print tokens
    program = Characters("input/input.txt")
    scanner = Scanner(table_dictionary)
    tokens = scanner.parse(program)
    for token in tokens:
        print(token)
