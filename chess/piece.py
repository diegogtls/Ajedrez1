
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

# Dama
class Queen(Piece):
    symbol = "Q"
    def get_moves(self, position, board):
        moves = []
        x, y = position
        
        # 8 direcciones: diagonales + rectas
        directions = [
            (-1, -1), (-1, 1), (1, -1), (1, 1),  # diagonales
            (-1, 0), (1, 0), (0, -1), (0, 1)     # rectas
        ]
        
        for dx, dy in directions:
            i, j = x + dx, y + dy
            while 0 <= i < 8 and 0 <= j < 8:  # mientras esté dentro del tablero
                target = board.grid[i][j]
                if target is None:  # casilla vacía
                    moves.append((i, j))
                elif target.color != self.color:  # pieza rival
                    moves.append((i, j))
                    break
                else:  # pieza propia
                    break
                # seguimos en la misma dirección
                i += dx
                j += dy
        
        return moves

# Rey
class King(Piece):
    symbol = "K"
    def get_moves(self, position, board):
        moves = []
        x, y = position

        # 8 direcciones posibles (diagonales + rectas)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        for dx, dy in directions:
            i, j = x + dx, y + dy
            # Solo una casilla en cada dirección
            if 0 <= i < 8 and 0 <= j < 8:
                target = board.grid[i][j]
                if target is None or target.color != self.color:
                    moves.append((i, j))

        return moves

# Peón
class Pawn(Piece):
    symbol = "P"

    def get_moves(self, position, board):
        moves = []
        x, y = position
        direction = -1 if self.color == "white" else 1  # blanco va hacia arriba, negro hacia abajo
        
        # Avanzar una casilla
        if 0 <= x + direction < 8 and board.grid[x + direction][y] is None:
            moves.append((x + direction, y))
            
            # Avanzar dos casillas desde la posición inicial
            start_row = 6 if self.color == "white" else 1
            if x == start_row and board.grid[x + 2 * direction][y] is None:
                moves.append((x + 2 * direction, y))

        # Capturas diagonales
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.grid[nx][ny]
                if target is not None and target.color != self.color:
                    moves.append((nx, ny))

        return moves