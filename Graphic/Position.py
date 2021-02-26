class Position:
    def __init__(self, row, col, obj=None):
        self.row = row
        self.col = col
        self.obj = obj

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
