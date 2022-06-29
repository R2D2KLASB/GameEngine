from .ai import AIPlayer

class LANAI(AIPlayer):
    def __init__(self, row_size, col_size, name):
        super().__init__(row_size, col_size, name)