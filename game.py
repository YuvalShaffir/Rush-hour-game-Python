from board import Board
from car import Car
from helper import load_json
import sys

class Game:
    """
    Add class description here
    """
    LEGAL_COLORS = ['Y', 'B', 'O', 'G', 'W', 'R']
    LEGAL_MOVES = ['u', 'd', 'r', 'l']

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it.

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        user_input = input("Enter Car color and direction\n")
        color = user_input[0]
        direction = user_input[2]
        while color not in Game.LEGAL_COLORS and direction not in Game.LEGAL_MOVES:
            user_input = input("WRONG INPUT! Enter Car color and direction\n")
            color = user_input[0]
            direction = user_input[2]
        self.board.move_car(color, direction)
        if self.board.target_is_empty():
            return True
        else:
            return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while self.__single_turn():
            print(self.board)
        print("You Won!")
        return

# todo: add descriptions to all methods and class and remove main.py


if __name__ == "__main__":
    """Runs the game"""
    board = Board()
    car_lst = load_json(sys.argv[1])
    # adds a legal car to the board
    for key, value in car_lst.items():
        name = key
        length = value[0]
        orientation = value[2]
        # checks if the values are legal to the game's rules:
        if key not in {'Y', 'B', 'O', 'G', 'W', 'R'} or length < 2 or 4 < length or orientation not in {0, 1}:
            continue
        location = value[1]
        car = Car(name, length, location, orientation)
        board.add_car(car)
    game = Game(board)
    print(board)
    game.play()




