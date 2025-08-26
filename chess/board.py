class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)] #Crea matriz de 8x8 vacía

    def place_piece(self, piece, position):
        x, y = position
        self.grid[x][y] = piece

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        if piece:
            self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None

    def is_empty(self, position):
        x, y = position
        return self.grid[x][y] is None
    
    def __str__(self):
        rows=[]
        for i in range(8):
            row=[]
            for j in range(8):
                if self.grid[i][j]:
                    row.append(str(self.grid[i][j]))
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)