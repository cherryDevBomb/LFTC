class ScannerTable:

    def __init__(self, symbols, incidence_matrix, start_state, end_states, symbol_dict):
        self.symbols = symbols
        self.incidence_matrix = incidence_matrix
        self.start_state = start_state
        self.end_states = end_states
        self.symbol_dict = symbol_dict
