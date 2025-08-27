from .board import Board
from .piece import Piece, Rook, Knight, Bishop, Queen, King, Pawn
from .player import Player

class Game:
    def __init__(self, player_white, player_black):
        self.board = Board()
        self.players = {"white": player_white, "black": player_black}
        self.turn = "white"  # empieza el turno de las blancas

        # Colocar piezas
        # Torres
        self.board.place_piece(Rook("white"), (7, 0))
        self.board.place_piece(Rook("white"), (7, 7))
        self.board.place_piece(Rook("black"), (0, 0))
        self.board.place_piece(Rook("black"), (0, 7))

        #Caballos
        self.board.place_piece(Knight("white"), (7, 1))
        self.board.place_piece(Knight("white"), (7, 6))
        self.board.place_piece(Knight("black"), (0, 1))
        self.board.place_piece(Knight("black"), (0, 6))

        #Alfiles
        self.board.place_piece(Bishop("white"), (7, 2))
        self.board.place_piece(Bishop("white"), (7, 5))
        self.board.place_piece(Bishop("black"), (0, 2))
        self.board.place_piece(Bishop("black"), (0, 5))

        #Damas
        self.board.place_piece(Queen("white"), (7, 3))
        self.board.place_piece(Queen("black"), (0, 3))

        #Reyes
        self.board.place_piece(King("white"), (7, 4))
        self.board.place_piece(King("black"), (0, 4))

        #Peones
        self.board.place_piece(Pawn("white"), (6, 0))
        self.board.place_piece(Pawn("white"), (6, 1))
        self.board.place_piece(Pawn("white"), (6, 2))
        self.board.place_piece(Pawn("white"), (6, 3))
        self.board.place_piece(Pawn("white"), (6, 4))
        self.board.place_piece(Pawn("white"), (6, 5))
        self.board.place_piece(Pawn("white"), (6, 6))
        self.board.place_piece(Pawn("white"), (6, 7))
        self.board.place_piece(Pawn("black"), (1, 0))
        self.board.place_piece(Pawn("black"), (1, 1))
        self.board.place_piece(Pawn("black"), (1, 2))
        self.board.place_piece(Pawn("black"), (1, 3))
        self.board.place_piece(Pawn("black"), (1, 4))
        self.board.place_piece(Pawn("black"), (1, 5))
        self.board.place_piece(Pawn("black"), (1, 6))
        self.board.place_piece(Pawn("black"), (1, 7))
    
    def switch_turn(self):
        """Cambia de turno entre blanco y negro"""
        self.turn = "black" if self.turn == "white" else "white"

    def current_player(self):
        """Devuelve el jugador actual"""
        return self.players[self.turn]

    def show_board(self):
        print(self.board)

    def available_moves(self, position):
        piece = self.board.grid[position[0]][position[1]]
        if piece and piece.color == self.turn:  # solo puede mover piezas de su color
            return piece.get_moves(position, self.board)
        return []
    
    def move(self, start, end):
        """
        Mueve la pieza si es legal.
        start y end son tuplas: (x, y)
        """
        piece = self.board.grid[start[0]][start[1]]
        if piece is None:
            print("No hay pieza en esa casilla.")
            return False
        if piece.color != self.turn:
            print(f"No es turno de {piece.color}.")
            return False

        if end not in piece.get_moves(start, self.board):
            print("Movimiento ilegal")
            return False

        # ---- Simular el movimiento ----
        original_target = self.board.grid[end[0]][end[1]] # Guardamos lo que había en la casilla de destino por si hay que deshacer la jugada
        self.board.move_piece(start, end)

        # Verificar si el rey queda en jaque
        if self.is_in_check(self.turn):
            # Deshacer el movimiento
            self.board.move_piece(end, start)
            self.board.grid[end[0]][end[1]] = original_target
            print("No puedes dejar a tu rey en jaque")
            return False

        # Promoción de peón
        if isinstance(piece, Pawn):
            final_row = 0 if piece.color == "white" else 7
            if end[0] == final_row:
                promoted_name = input_piece("Peón promocionado! Elige: Queen, Rook, Bishop o Knight: ")

                # Instanciar la pieza con el color correcto automáticamente
                if promoted_name == "Queen":
                    promoted_piece = Queen(piece.color)
                elif promoted_name == "Rook":
                    promoted_piece = Rook(piece.color)
                elif promoted_name == "Bishop":
                    promoted_piece = Bishop(piece.color)
                else:  # Knight
                    promoted_piece = Knight(piece.color)

                # Reemplazar el peón en el tablero
                self.board.grid[end[0]][end[1]] = promoted_piece

        # Si es válido, cambiar turno
        self.switch_turn()
        return True

            # Promoción de peón
            if isinstance(piece, Pawn):
                final_row = 0 if piece.color == "white" else 7
                if end[0] == final_row:
                    promoted_name = input_piece("Peón promocionado! Elige: Queen, Rook, Bishop o Knight: ")

                    # Instanciar la pieza con el color correcto automáticamente
                    if promoted_name == "Queen":
                        promoted_piece = Queen(piece.color)
                    elif promoted_name == "Rook":
                        promoted_piece = Rook(piece.color)
                    elif promoted_name == "Bishop":
                        promoted_piece = Bishop(piece.color)
                    else:  # Knight
                        promoted_piece = Knight(piece.color)

                    # Reemplazar el peón en el tablero
                    self.board.grid[end[0]][end[1]] = promoted_piece

            self.switch_turn()
            return True
        else:
            print("Movimiento ilegal.")
            return False

    def is_in_check(self, color):
        # Buscar la posición del rey
        for x in range(8):
            for y in range(8):
                piece = self.board.grid[x][y]
                if piece is not None and isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break

        # Revisar movimientos de todas las piezas enemigas
        enemy_color = "black" if color == "white" else "white"
        for x in range(8):
            for y in range(8):
                piece = self.board.grid[x][y]
                if piece is not None and piece.color == enemy_color:
                    if king_pos in piece.get_moves((x, y), self.board):
                        return True  # Rey atacado
        return False


    