from collections import Counter
import hashlib

letras = "abcdefgh"

def from_algebraic(square):
    y = letras.index(square[0])
    x = 8 - int(square[1])
    return (x, y)

def to_algebraic(pos):
    x, y = pos
    return f"{letras[y]}{8 - x}"

def input_square(prompt):
    while True:
        square = input(prompt).strip()
        if len(square) == 2 and square[0] in "abcdefgh" and square[1] in "12345678":
            return square
        print("Entrada inválida. Usa formato como 'a1', 'b2', etc.")

def input_piece(prompt):
    while True:
        piece = input(prompt)
        if piece in ("Queen", "Rook", "Bishop", "knight"):
            return piece
        print("Entrada inválida. Elige una pieza: Queen, Rook, Bishop o knight: ")

def square_color(position):
    x, y = position
    return "dark" if (x + y) % 2 == 0 else "light"

def count_pieces(board):
    white_counts = Counter()
    black_counts = Counter()
    for i in range(8):
        for j in range(8):
            piece = board.grid[i][j]
            if piece is None:
                continue
            counter = white_counts if piece.color == "white" else black_counts
            counter[type(piece).__name__] += 1

    return white_counts, black_counts

def find_piece_position(board, color, piece_type_name):
    for i in range(8):
        for j in range(8):
            piece = board.grid[i][j]
            if piece is not None and piece.color == color and type(piece).__name__ == piece_type_name:
                return (i, j)

def board_signature(board, turn):
    """
    Devuelve una firma única (hash SHA256) de la posición actual del tablero,
    usando notación FEN simplificada (solo piezas y casillas vacías).
    """
    rows = []
    for i in range(8):
        row = ""
        empty_count = 0
        for j in range(8):
            piece = board.grid[i][j]
            if piece is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    row += str(empty_count)
                    empty_count = 0
                symbol = piece.symbol.upper() if piece.color == "white" else piece.symbol.lower()
                row += symbol
        if empty_count > 0:  # cerrar la fila si termina con vacías
            row += str(empty_count)
        rows.append(row)

    # Unir filas como en FEN
    fen_position = "/".join(rows)

    # Añadir el turno (w o b) para distinguir posiciones
    fen_with_turn = fen_position + " " + ("w" if turn == "white" else "b")

    # Devolver hash seguro
    return hashlib.sha256(fen_with_turn.encode()).hexdigest()