files = "abcdefgh"

def from_algebraic(square):
    y = files.index(square[0])
    x = 8 - int(square[1])
    return (x, y)

def to_algebraic(pos):
    x, y = pos
    return f"{files[y]}{8 - x}"

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