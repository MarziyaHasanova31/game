import random
import unittest

class Ship:
    """Класс, представляющий корабль.

     Args:
         x (int): Координата X корабля на игровой доске.
         y (int): Координата Y корабля на игровой доске.
         length (int): Длина корабля.
         direction (str): Направление корабля ('h' - горизонтально, 'v' - вертикально).

     Attributes:
         x (int): Координата X корабля на игровой доске.
         y (int): Координата Y корабля на игровой доске.
         length (int): Длина корабля.
         direction (str): Направление корабля ('h' - горизонтально, 'v' - вертикально).
         hits (int): Количество попаданий по кораблю.

     Methods:
         hit(): Обрабатывает попадание по кораблю и возвращает статус поражения или ранения.
     """
    def __init__(self, x, y, length, direction):
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        self.hits = 0

    def hit(self):
        self.hits += 1
        if self.hits == self.length:
            return "Уничтожен"
        else:
            return "Ранил!"


class GameBoard:
    """Класс, представляющий игровую доску.

      Args:
          size (int): Размер игровой доски (например, 10 для доски 10x10 клеток).

      Attributes:
          size (int): Размер игровой доски.
          board (list): Двумерный список, представляющий игровую доску.

      Methods:
          place_ship(ship): Размещает корабль на игровой доске.
          is_valid_move(x, y): Проверяет, является ли данное перемещение допустимым.
          is_hit(x, y): Проверяет, было ли попадание по указанным координатам.
          attack(x, y): Обрабатывает атаку игрока и возвращает результат (попадание или промах).
      """
    def __init__(self, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]


    def place_ship(self, ship):

        if ship.direction == "h":
            for i in range(ship.length):
                self.board[ship.y][ship.x + i] = 1
        else:
            for i in range(ship.length):
                self.board[ship.y + i][ship.x] = 1

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_hit(self, x, y):
        return self.board[y][x] == 1

    def attack(self, x, y):
        if self.is_valid_move(x, y):
            if self.board[y][x] == 1:
                self.board[y][x] = 2
                return "Hit"
            else:
                self.board[y][x] = 3
                return "Miss"

"""Класс, представляющий игрока.

Args:
    name (str): Имя игрока.
    board (GameBoard): Игровая доска, на которой размещаются корабли.

Attributes:
    name (str): Имя игрока.
    board (GameBoard): Игровая доска игрока.

Methods:
    place_ships(ship_list): Размещает корабли из списка на игровой доске игрока.
"""
class Player:
    def __init__(self, name, board):
        self.name = name
        self.board = board

    def place_ships(self, ship_list):
        for ship in ship_list:
            valid_placement = False
            while not valid_placement:
                x = random.randint(0, self.board.size - 1)
                y = random.randint(0, self.board.size - 1)
                direction = random.choice(["h", "v"])
                ship.x, ship.y, ship.direction = x, y, direction
                if self.board.is_valid_move(x, y):
                    if direction == "h" and x + ship.length <= self.board.size and all(
                            el == 0 for el in self.board.board[y][x:x + ship.length]):
                        for i in range(ship.length):
                            self.board.board[y][x + i] = 1
                        valid_placement = True
                    elif direction == "v" and y + ship.length <= self.board.size and all(
                            self.board.board[i][x] == 0 for i in range(y, y + ship.length)):
                        for i in range(ship.length):
                            self.board.board[y + i][x] = 1
                        valid_placement = True


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0

    def switch_player(self):
        self.current_player = (self.current_player + 1) % 2

    def play_turn(self, x, y):
        other_player = (self.current_player + 1) % 2
        result = self.players[other_player].board.attack(x, y)
        self.switch_player()
        return result

    def is_game_over(self):
        for player in self.players:
            for row in player.board.board:
                if 1 in row:
                    return False
        return True

class TestShipPlacement(unittest.TestCase):
    def setUp(self):
        self.board = GameBoard(10)
        self.player = Player("Test Player", self.board)

    def test_ship_placement(self):
        ship = Ship(0, 0, 1, "h")
        self.player.place_ships([ship])
        self.assertEqual(self.board.board[0][0:3], [0, 0, 0 ])


if __name__ == '__main':
    unittest.main()


# пример игры
player1 = Player("Player 1", GameBoard(10))
player2 = Player("Player 2", GameBoard(10))

game = Game(player1, player2)

ship1_p1 = Ship(0, 0, 3, "h")
ship2_p1 = Ship(4, 5, 4, "v")
player1.place_ships([ship1_p1, ship2_p1])

ship1_p2 = Ship(2, 3, 3, "v")
ship2_p2 = Ship(7, 8, 5, "h")
player2.place_ships([ship1_p2, ship2_p2])

while not game.is_game_over():
    print(f"It's {game.players[game.current_player].name}'s turn.")
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    print(game.play_turn(x, y))
