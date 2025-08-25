from .board import Board
from .piece import Piece, Rook, Knight, Bishop
from .player import Player

class Game:
    def __init__(self, player_white, player_black):
        self.board = Board()
        self.players = {"white": player_white, "black": player_black}
        self.turn = "white"  # empieza el turno de las blancas

        # Colocar piezas
        # Torres
        self.board.place_piece(Rook("white"), (0, 0))
        self.board.place_piece(Rook("white"), (0, 7))
        self.board.place_piece(Rook("black"), (7, 0))
        self.board.place_piece(Rook("black"), (7, 7))

        #Caballos
        self.board.place_piece(Knight("white"), (0, 1))
        self.board.place_piece(Knight("white"), (0, 6))
        self.board.place_piece(Knight("black"), (7, 1))
        self.board.place_piece(Knight("black"), (7, 6))

        #Alfiles
        self.board.place_piece(Bishop("white"), (0, 2))
        self.board.place_piece(Bishop("white"), (0, 5))
        self.board.place_piece(Bishop("black"), (7, 2))
        self.board.place_piece(Bishop("black"), (7, 5))
    
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
        
        if end in piece.get_moves(start, self.board):
            self.board.move_piece(start, end)
            self.switch_turn()
            return True
        else:
            print("Movimiento ilegal.")
            return False


    