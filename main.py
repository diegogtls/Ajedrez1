from chess.game import Game
from chess.player import Player
from chess.utils import from_algebraic, to_algebraic, input_square

if __name__ == "__main__":
    
    print("=== Bienvenido al ajedrez ===\n")

    nombre1 = input("Nombre jugador blancas: ")
    nombre2 = input("Nombre jugador negras: ")

    player1 = Player(nombre1, "white")
    player2 = Player(nombre2, "black")

    game = Game(player1, player2)


    while True:

        game.show_board()
        player = game.current_player()
        print(f"Turno de: {player.name} ({player.color})")

        start_square = input_square("Selecciona la pieza a mover (ej: a1): ")
        end_square = input_square("Selecciona la casilla destino (ej: a4): ")

        start = from_algebraic(start_square)
        end = from_algebraic(end_square)

        moved = game.move(start, end)
        if moved:
            print("Movimiento realizado ✅\n")
        else:
            print("Intenta otro movimiento ❌\n")
        if game.winner is not None:
            if game.winner == "draw":
                print(f"🤝 La partida ha terminado en tablas ¡Gracias por jugar! 🏁")
            else:
                print(f"¡Jaque mate! {game.winner.name}({game.winner.color}) gana la partida 🎉 ¡Gracias por jugar! 🏁")
            break
