from Lab3.neatodea import delta
from Lab5.scanner_table import ScannerTable


symbol_groups = {
        'alpha': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'digit1_9': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        'zero': ['0'],
        'digit': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        'other': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '}', '{', '|', '\\', ':', ';', '<', '>', ',', '.', '?', ' '],
        'symbol': ['+', '-', '*', '/', '<', '>', '=', ':', '%', '!'],
        'slash': ['/'],
        'dot': ['.']
    }


def create_scanner_table(ea, output_name):
    # symbol classes
    with open(output_name, 'w') as file:
        for char in ea.edge_labels:
            file.write(char + '\t')
        file.write('\n')

        # number of states
        file.write(str(len(ea.nodes)) + '\n')

        # delta values for each state with each symbol class
        incidence_matrix = []
        for z in ea.nodes:
            z_values = []
            for c in ea.edge_labels:
                delta_result = delta(ea, [z], c)
                if len(delta_result) == 0:
                    result = "err"
                else:
                    result = list(delta_result)[0].id
                file.write(str(result) + '\t')
                z_values.append(result)
            file.write('\n')
            incidence_matrix.append(z_values)

        # end nodes
        for end_node in ea.get_end_nodes():
            file.write(str(end_node.id) + '\t')
        file.write('\n')

        # symbol dictionaries that belong to this class
        my_groups = {}
        for group in symbol_groups:
            if group in ea.edge_labels:
                for char in symbol_groups[group]:
                    file.write(char)
                file.write('\n')
                my_groups[group] = symbol_groups[group]

        start_state = ea.get_start_node().id
        end_states = [node.id for node in ea.get_end_nodes()]
        scanner_table = ScannerTable(ea.edge_labels, incidence_matrix, start_state, end_states, my_groups)
    return scanner_table
