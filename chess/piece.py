class Piece:
    def __init__(self, color):
        self.color = color #"white" o "black"

    def get_moves(self, position, board):
        raise NotImplementedError
    def __str__(self):
        return self.symbol

# Torre
class Rook(Piece):
    symbol = "R"
    def get_moves(self, position, board):
        moves = []
        x, y = position # Consideramos el 0,0 en la esquina superior izquierda x mueve vertical, y mueve horizontal

        # Arriba
        for i in range(x - 1, -1, -1):
            target = board.grid[i][y]
            if target is None:  # casilla vacía
                moves.append((i, y))
            elif target.color != self.color:  # pieza rival
                moves.append((i, y))
                break
            else:  # pieza propia
                break
        
        # Abajo
        for i in range(x + 1, 8):
            target = board.grid[i][y]
            if target is None:  # casilla vacía
                moves.append((i, y))
            elif target.color != self.color:  # pieza rival
                moves.append((i, y))
                break
            else:  # pieza propia
                break
        
        # Izquierda
        for j in range(y - 1, -1, -1):
            target = board.grid[x][j]
            if target is None:  # casilla vacía
                moves.append((x, j))
            elif target.color != self.color:  # pieza rival
                moves.append((x, j))
                break
            else:  # pieza propia
                break

        # Derecha
        for j in range(y + 1, 8):
            target = board.grid[x][j]
            if target is None:  # casilla vacía
                moves.append((x, j))
            elif target.color != self.color:  # pieza rival
                moves.append((x, j))
                break
            else:  # pieza propia
                break

        return moves

# Caballo
class Knight(Piece):
    symbol = "N"
    def get_moves(self, position, board):
        moves = []
        x, y = position # Consideramos el 0,0 en la esquina superior izquierda

        # Movimientos del caballo (8 posibles)
        potential_moves = [
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x - 2, y + 1),
            (x - 2, y - 1),
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2)
        ]
        for mx, my in potential_moves:
            if 0 <= mx < 8 and 0 <= my < 8:
                target = board.grid[mx][my]
                if target is None or target.color != self.color:
                    moves.append((mx, my))
                    
        return moves

# Alfil
class Bishop(Piece):
    symbol = "B"
    def get_moves(self, position, board):
        moves = []
        x, y = position # Consideramos el 0,0 en la esquina superior izquierda

        # Arriba-Izquierda
        for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            target = board.grid[i][j]
            if target is None:  # casilla vacía
                moves.append((i, j))
            elif target.color != self.color:  # pieza rival
                moves.append((i, j))
                break
            else:  # pieza propia
                break

        # Arriba-Derecha
        for i, j in zip(range(x + 1, 8), range(y - 1, -1, -1)):
            target = board.grid[i][j]
            if target is None:  # casilla vacía
                moves.append((i, j))
            elif target.color != self.color:  # pieza rival
                moves.append((i, j))
                break
            else:  # pieza propia
                break

        # Abajo-Izquierda
        for i, j in zip(range(x - 1, -1, -1), range(y + 1, 8)):
            target = board.grid[i][j]
            if target is None:  # casilla vacía
                moves.append((i, j))
            elif target.color != self.color:  # pieza rival
                moves.append((i, j))
                break
            else:  # pieza propia
                break

        # Abajo-Derecha
        for i, j in zip(range(x + 1, 8), range(y + 1, 8)):
            target = board.grid[i][j]
            if target is None:  # casilla vacía
                moves.append((i, j))
            elif target.color != self.color:  # pieza rival
                moves.append((i, j))
                break
            else:  # pieza propia
                break
                
        return moves