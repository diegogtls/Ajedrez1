from .board import Board
from .piece import Piece, Rook, Knight, Bishop, Queen, King, Pawn
from .player import Player
from .utils import count_pieces, square_color, find_piece_position, board_signature
from collections import Counter

class Game:
    def __init__(self, player_white, player_black):
        self.board = Board()
        self.players = {"white": player_white, "black": player_black}
        self.turn = "white"  # empieza el turno de las blancas
        self.winner = None # None = partida en curso, "draw" = tablas, Player = ganador
        self.turn_count = 1 # Contador general de turnos
        self.fifty_move_counter = 0 # Contador de turnos para la regla de los 50 movimientos
        self.signatures = Counter()

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

    def has_legal_moves(self, color):
        """Devuelve True si el jugador 'color' tiene al menos un movimiento legal."""
        for i in range(8):
            for j in range(8):
                piece = self.board.grid[i][j]
                if piece is None or piece.color != color:
                    continue
                for end in piece.get_moves((i, j), self.board):
                    # Guardar estado previo
                    original = self.board.grid[end[0]][end[1]]
                    self.board.move_piece((i, j), end)
                    if not self.is_in_check(color):
                        # Deshacer y devolver True
                        self.board.move_piece(end, (i, j))
                        self.board.grid[end[0]][end[1]] = original
                        return True
                    # Deshacer movimiento
                    self.board.move_piece(end, (i, j))
                    self.board.grid[end[0]][end[1]] = original
        return False

    def switch_turn(self):
        """Cambia de turno entre blanco y negro"""
        self.turn = "black" if self.turn == "white" else "white"
        self.turn_count += 1

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
                promotions = {
                    "Queen": Queen,
                    "Rook": Rook,
                    "Bishop": Bishop,
                    "Knight": Knight
                }
                promoted_piece = promotions[promoted_name](piece.color)

                # Reemplazar el peón en el tablero
                self.board.grid[end[0]][end[1]] = promoted_piece
        
        # Guarda la posición del tablero
        sig = board_signature(self.board, self.turn)
        self.signatures[sig] += 1

        #Verificación contador 50 movimientos para tablas
        if isinstance(piece, Pawn) or original_target is not None:
            self.fifty_move_counter = 0  # reinicia al mover peón o capturar
        else:
            self.fifty_move_counter += 1  # incrementa en cualquier otro movimiento

        # Verificación jaque mate y tablas
        enemy_color = "black" if self.turn == "white" else "white"

        if self.is_checkmate(enemy_color):
            self.winner = self.current_player()
        elif self.is_draw(enemy_color):
            self.winner = "draw"
        else:
            self.switch_turn()

        return True

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

    def is_checkmate(self, enemy_color):
        """Devuelve True si el jugador 'enemy_color' está en jaque mate"""
        return self.is_in_check(enemy_color) and not self.has_legal_moves(enemy_color)

    def is_draw(self, enemy_color):
        """Devuelve True si son tablas"""

        # Rey Ahogado
        if not self.is_in_check(enemy_color) and not self.has_legal_moves(enemy_color):
            return True

        # Material insuficiente
        white_counts, black_counts = count_pieces(self.board)

        # Rey vs Rey
        if white_counts == {"King": 1} and black_counts == {"King": 1}:
            return True

        # Rey + alfil vs Rey
        if ("Bishop" in white_counts and len(white_counts) == 2 and black_counts == {"King": 1}) \
        or ("Bishop" in black_counts and len(black_counts) == 2 and white_counts == {"King": 1}):
            return True

        # Rey + Caballo vs Rey
        if ("Knight" in white_counts and len(white_counts) == 2 and black_counts == {"King": 1}) \
        or ("Knight" in black_counts and len(black_counts) == 2 and white_counts == {"King": 1}):
            return True

        # Rey + alfil vs Rey + alfil (alfiles en casillas del mismo color)
        if ("Bishop" in white_counts and len(white_counts) == 2 and "Bishop" in black_counts and len(black_counts) == 2):
            white_bishop_pos = find_piece_position(self.board, "white", "Bishop")
            black_bishop_pos = find_piece_position(self.board, "black", "Bishop")
            if square_color(white_bishop_pos) == square_color(black_bishop_pos):
                return True

        # Misma posición del tablero 3 veces
        if any(count >= 3 for count in self.signatures.values()):
            return True

        # No hay movimiento de peón ni capturas en 50 movimientos consecutivos
        if self.fifty_move_counter >= 100:  # 100 medias jugadas = 50 turnos
            return True  # tablas por regla de 50 movimientos

        # si no se cumple ninguna de las anteriores: no hay tablas
        return False